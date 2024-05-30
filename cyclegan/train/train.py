from IPython.display import clear_output

from collections import defaultdict
import numpy as np
import torch
import torch.optim as optim
import torch.nn.functional as F
from tqdm.auto import trange

from cyclegan.train.utils import *

def train_discriminators(model, opt_d, loader_a, loader_b, criterion_d, device='cuda'):
    model.train()
    losses_tr = []

    iter_a = iter(loader_a)
    iter_b = iter(loader_b)
    batches_per_epoch = min(len(iter_a), len(iter_b))

    for _ in trange(batches_per_epoch):
        imgs_a = next(iter_a).to(device)
        imgs_b = next(iter_b).to(device)

        opt_d.zero_grad()

        a_real_pred = model.D_A(imgs_a)
        b_real_pred = model.D_B(imgs_b)

        fake_a = model.G_BA(imgs_b).detach()
        fake_b = model.G_AB(imgs_a).detach()

        a_fake_pred = model.D_A(fake_a)
        b_fake_pred = model.D_B(fake_b)

        loss = criterion_d(a_real_pred, b_real_pred, a_fake_pred, b_fake_pred)

        loss.backward()
        opt_d.step()
        losses_tr.append(loss.item())

    return model, opt_d, np.mean(losses_tr)


def train_generators(model, opt_g, loader_a, loader_b, criterion_g, device='cuda'):
    model.train()
    losses_tr = []

    iter_a = iter(loader_a)
    iter_b = iter(loader_b)
    batches_per_epoch = min(len(iter_a), len(iter_b))

    for _ in trange(batches_per_epoch):
        imgs_a = next(iter_a).to(device)
        imgs_b = next(iter_b).to(device)

        opt_g.zero_grad()

        fake_a = model.G_BA(imgs_b)
        fake_b = model.G_AB(imgs_a)

        rec_a = model.G_BA(fake_b)
        rec_b = model.G_AB(fake_a)

        a_fake_pred = model.D_A(fake_a.detach())
        b_fake_pred = model.D_B(fake_b.detach())

        loss = criterion_g(imgs_a, imgs_b, rec_a, rec_b, a_fake_pred, b_fake_pred)

        loss.backward()
        opt_g.step()
        losses_tr.append(loss.item())

    return model, opt_g, np.mean(losses_tr)

def val(model, loader_a, loader_b, criterion_d, criterion_g, device='cuda'):
    model.eval()

    val_data = defaultdict(list)

    with torch.no_grad():
        iter_a = iter(loader_a)
        iter_b = iter(loader_b)
        batches_per_epoch = min(len(iter_a), len(iter_b))

        for _ in trange(batches_per_epoch):
            imgs_a = next(iter_a).to(device)
            imgs_b = next(iter_b).to(device)

            a_real_pred = model.D_A(imgs_a)
            b_real_pred = model.D_B(imgs_b)

            fake_a = model.G_BA(imgs_b)
            fake_b = model.G_AB(imgs_a)

            rec_a = model.G_BA(fake_b)
            rec_b = model.G_AB(fake_a)

            a_fake_pred = model.D_A(fake_a)
            b_fake_pred = model.D_B(fake_b)

            loss_d = criterion_d(a_real_pred, b_real_pred, a_fake_pred, b_fake_pred)

            loss_g = criterion_g(imgs_a, imgs_b, rec_a, rec_b, a_fake_pred, b_fake_pred)

            val_data["loss D"].append(loss_d.item())
            val_data["loss G"].append(loss_g.item())

            is_mse_pred = a_real_pred.shape[-1] == 1

            if is_mse_pred:
                a_real_pred = a_real_pred[:, 0]
                b_real_pred = b_real_pred[:, 0]
                a_fake_pred = a_fake_pred[:, 0]
                b_fake_pred = b_fake_pred[:, 0]
            else:
                a_real_pred = F.softmax(a_real_pred, dim=1)[:, 1]
                b_real_pred = F.softmax(b_real_pred, dim=1)[:, 1]
                a_fake_pred = F.softmax(a_fake_pred, dim=1)[:, 1]
                b_fake_pred = F.softmax(b_fake_pred, dim=1)[:, 1]

            val_data["real pred A"].extend(a_real_pred.cpu().detach().tolist())
            val_data["real pred B"].extend(b_real_pred.cpu().detach().tolist())
            val_data["fake pred A"].extend(a_fake_pred.cpu().detach().tolist())
            val_data["fake pred B"].extend(b_fake_pred.cpu().detach().tolist())

        val_data["loss D"] = np.mean(val_data["loss D"])
        val_data["loss G"] = np.mean(val_data["loss G"])

    return val_data


def learning_loop(
    model,
    optimizer_g,
    g_iters_per_epoch,
    optimizer_d,
    d_iters_per_epoch,
    train_loader_a,
    train_loader_b,
    val_loader_a,
    val_loader_b,
    criterion_d,
    criterion_g,
    de_norm_a,
    de_norm_b,
    scheduler_d=None,
    scheduler_g=None,
    min_lr=None,
    epochs=10,
    val_every=1,
    draw_every=1,
    model_name=None,
    chkp_folder="./chkps",
    images_per_validation=3,
    plots=None,
    starting_epoch=0
):
    model_name = get_model_name(chkp_folder, model_name)

    if plots is None:
        plots = {
            'train G': [],
            'train D': [],
            'val D': [],
            'val G': [],
            "lr G": [],
            "lr D": [],
            "hist real A": [],
            "hist gen A": [],
            "hist real B": [],
            "hist gen B": [],
        }

    for epoch in np.arange(1, epochs+1) + starting_epoch:
        print(f'#{epoch}/{epochs}:')

        plots['lr G'].append(get_lr(optimizer_g))
        plots['lr D'].append(get_lr(optimizer_d))

        # Train discriminators
        print(f"train discriminators ({d_iters_per_epoch} times)")
        loss_d = []
        for _ in range(d_iters_per_epoch):
            model, optimizer_d, loss = train_discriminators(model, optimizer_d, train_loader_a, train_loader_b, criterion_d)
            loss_d.append(loss)
        plots['train D'].extend(loss_d)

        # Train generators
        print(f"train generators ({g_iters_per_epoch} times)")
        loss_g = []
        for _ in range(g_iters_per_epoch):
            model, optimizer_g, loss = train_generators(model, optimizer_g, train_loader_a, train_loader_b, criterion_g)
            loss_g.append(loss)
        plots['train G'].extend(loss_g)

        # Log training metrics to wandb
        wandb.log({
            "Train Discriminator Loss": np.mean(loss_d),
            "Train Generator Loss": np.mean(loss_g),
            "Learning Rate D": get_lr(optimizer_d),
            "Learning Rate G": get_lr(optimizer_g),
            "Epoch": epoch
        })

        if not (epoch % val_every):
            print("validate")
            val_data = val(model, val_loader_a, val_loader_b, criterion_d, criterion_g)
            plots['val D'].append(val_data["loss D"])
            plots['val G'].append(val_data["loss G"])
            plots['hist real A'].append(val_data["real pred A"])
            plots['hist gen A'].append(val_data["fake pred A"])
            plots['hist real B'].append(val_data["real pred B"])
            plots['hist gen B'].append(val_data["fake pred B"])

            clear_output(True)

            hh = 1
            ww = 2
            plt_ind = 1
            fig, ax = plt.subplots(hh, ww, figsize=(25, 12))
            fig.suptitle(f'#{epoch}/{epochs}:')

            plt.subplot(hh, ww, plt_ind)
            plt.title("Discriminator A predictions")
            plt.hist(plots["hist real A"][-1], bins=50, density=True, label="real", color="green", alpha=0.7)
            plt.hist(plots["hist gen A"][-1], bins=50, density=True, label="generated", color="red", alpha=0.7)
            plt.xlim((-0.05, 1.05))
            plt.xticks(ticks=np.arange(0, 1.05, 0.1))
            plt.legend()
            plt_ind += 1

            plt.subplot(hh, ww, plt_ind)
            plt.title("Discriminator B predictions")
            plt.hist(plots["hist real B"][-1], bins=50, density=True, label="real", color="green", alpha=0.7)
            plt.hist(plots["hist gen B"][-1], bins=50, density=True, label="generated", color="red", alpha=0.7)
            plt.xlim((-0.05, 1.05))
            plt.xticks(ticks=np.arange(0, 1.05, 0.1))
            plt.legend()
            plt_ind += 1

            plt.show()

            # Log validation metrics to wandb
            wandb.log({
                "Validation Discriminator Loss": val_data["loss D"],
                "Validation Generator Loss": val_data["loss G"], 
                "Epoch": epoch
            })

            draw_imgs(model, images_per_validation, val_loader_a, val_loader_b, de_norm_a, de_norm_b)

            # Save model checkpoint
            if not os.path.exists(chkp_folder):
                os.makedirs(chkp_folder)
            torch.save(
                {
                    'epoch': epoch,
                    'model_state_dict': model.state_dict(),
                    'optimizer_d_state_dict': optimizer_d.state_dict(),
                    'optimizer_g_state_dict': optimizer_g.state_dict(),
                    'scheduler_d_state_dict': scheduler_d.state_dict(),
                    'scheduler_g_state_dict': scheduler_g.state_dict(),
                    'plots': plots,
                },
                os.path.join(chkp_folder, model_name + '.pt'),
            )
            
            save_model(epoch, model_name, model)

            # Scheduler step
            if scheduler_d:
                try:
                    scheduler_d.step()
                except:
                    scheduler_d.step(loss_d)
            if scheduler_g:
                try:
                    scheduler_g.step()
                except:
                    scheduler_g.step(loss_g)

        if min_lr and get_lr(optimizer_d) <= min_lr:
            print(f'Learning process ended with early stop for discriminator after epoch {epoch}')
            break

        if min_lr and get_lr(optimizer_g) <= min_lr:
            print(f'Learning process ended with early stop for generator after epoch {epoch}')
            break

    wandb.finish()
    return model, optimizer_d, optimizer_g, plots


def create_model_and_optimizer(model_class, model_params, lr=2e-4, betas=(0.5, 0.999), device='cuda'):
    model = model_class(**model_params)
    model.to(device)

    optimizer_d = optim.Adam(
        list(model.D_A.parameters()) + list(model.D_B.parameters()),
        lr=lr,
        betas=betas
    )
    optimizer_g = optim.Adam(
        list(model.G_AB.parameters()) + list(model.G_BA.parameters()),
        lr=lr,
        betas=betas
    )
    return model, optimizer_d, optimizer_g
