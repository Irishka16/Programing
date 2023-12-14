import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons
import scipy.signal as sc


# створюються скелет діаграм
noise_base = 0
noise_cov = 0

noise = np.random.normal(0, noise_base, 1000)
t = np.linspace(0, 1, 1000)
fig, (ax1) = plt.subplots(1, 1)
# базова гармоніка
line, = ax1.plot(t, 5 * np.sin(5 * t + 1), lw=2)
# "зашумлена" гармоніка
line1, = ax1.plot(t, 5 * np.sin(5 * t + 1), lw=2, visible=False, alpha=0.5)
fig.subplots_adjust(left=0.15, bottom=0.3)


# створюємо слайдер для частоти
axfreq = fig.add_axes([0.25, 0.25, 0.55, 0.03])
fr_slider = Slider(
    ax=axfreq,
    label='Frequency',
    valmin=0.1,
    valmax=30,
    valinit=5,
)
# створюємо слайдер для амплітуди

axamp = fig.add_axes([0.25, 0.05, 0.55, 0.03])
amp_slider = Slider(
    ax=axamp,
    label="Amplitude",
    valmin=0,
    valmax=10,
    valinit=5
)
# створєюмо слайдер для шума
axamp1 = fig.add_axes([0.25, 0.15, 0.55, 0.03])
noise_mean_slider = Slider(
    ax=axamp1,
    label="Noise",
    valmin=0,
    valmax=2,
    valinit=0,
)
# створюємо слайдер для дисперсії шума 
axfs = fig.add_axes([0.25, 0.1, 0.55, 0.03])
noise_cov_slider = Slider(
    ax=axfs,
    label='Noise covariance',
    valmin=0.1,
    valmax=30,
    valinit=5,
)
# створюємо слайдер для дисперсії фази 

axwn = fig.add_axes([0.25, 0.2, 0.55, 0.03])
phase_slider = Slider(
    ax=axwn,
    label='Phas',
    valmin=0.1,
    valmax=10,
    valinit=0.1
)

# створюємо кнопку відображення шуму
ax_noise_toggle = fig.add_axes([0.8, 0.15, 0.1, 0.04])
noise_toggle_button = CheckButtons(ax=ax_noise_toggle, labels=['Show noise'], actives=[False])

resetax = fig.add_axes([0.9, 0.025, 0.1, 0.04])
reset_button = Button(resetax, 'Reset', hovercolor='0.975')

# функція гармоніки
def harmonic_with_noise(amplitude, frequency, phase=1, noise_mean=0, show_noise=True,noise_cov=1.05, ):
    if show_noise:
        line.set_ydata(amplitude * np.sin(2*np.pi*frequency * t + phase))
        line1.set_ydata(amplitude * np.sin(2*np.pi*frequency * t + phase) + noise_mean)
        line1.set_visible(True)
    else:
        line.set_ydata(amplitude * np.sin(2*np.pi*frequency * t + phase))
        line1.set_ydata(amplitude * np.sin(2*np.pi*frequency * t + phase)+noise_mean)
        line1.set_visible(False)
    fig.canvas.draw_idle()

# функція оновлення графіку, яка перебудовує графік при зміні слайдера
def update(val):
    global noise_base
    global noise
    global noise_cov
    if (noise_base != noise_mean_slider.val) or (noise_cov != noise_cov_slider.val):
        noise_base = noise_mean_slider.val
        noise_cov = noise_cov_slider.val

        noise = np.random.normal(noise_mean_slider.val,np.sqrt(noise_cov_slider.val) , 1000)
    harmonic_with_noise(amp_slider.val, fr_slider.val, noise_mean=noise,phase=phase_slider.val,
                noise_cov=noise_cov_slider.val,show_noise=noise_toggle_button.get_status()[0] )

# викликаємо функцію оновленя графіку при зміні будь якого зі слайдерів
fr_slider.on_changed(update)
amp_slider.on_changed(update)
noise_mean_slider.on_changed(update)
phase_slider.on_changed(update)
noise_toggle_button.on_clicked(update)
noise_cov_slider.on_changed(update)


# функція скиданння налаштувань
def reset(event):
    fr_slider.reset()
    amp_slider.reset()
    noise_mean_slider.reset()
    if noise_toggle_button.get_status()[0]:
        noise_toggle_button.set_active(0)

# викликаємо функція скиданння налаштувань при натисканні на кнопку Reset
reset_button.on_clicked(reset)
plt.show()