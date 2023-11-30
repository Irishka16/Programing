import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, Slider, CheckButtons

def harmonic_function(t, amplitude, frequency, phase, noise_mean, noise_covariance, show_noise):
    harmonic = amplitude * np.sin(2 * np.pi * frequency * t + phase)
    if show_noise:
        noise = np.random.normal(noise_mean, np.sqrt(noise_covariance), size=len(t))
        return harmonic + noise
    else:
        return harmonic

def update(val):
    # print(sliders['show_noise'].get_status())
    line.set_ydata(harmonic_function(t, amplitude=sliders['amplitude'].val, frequency=sliders['frequency'].val,
                                    phase=sliders['phase'].val, noise_mean=sliders['noise mean'].val, noise_covariance=sliders['noise covariance'].val,
                                    show_noise=sliders['show_noise'].get_status()[0]))
    fig.canvas.draw_idle()

def create_slider(ax, label, valmin,valmax,valinit,update_function=update):
    slider = Slider(ax,label,valmin,valmax,valinit)
    slider.on_changed(update_function)
    return slider

def toggle_noise(label):
    update(None)

def reset(event):
    for slider in sliders.values():
        if isinstance(slider, Slider):
            slider.reset()
        elif isinstance(slider, CheckButtons):
            for i in range(len(slider.labels)):
                slider.set_active(i)
    update(None)


# Define initial parameters
initial_parameters = {
    "amplitude" : 1.0,
    "frequency" :1.0,
    "phase" : 0.0,
    "noise_mean" : 0.0,
    "noise_covariance" : 0.0,
    "show_noise" : True
}
t = np.linspace(0, 1, 1000)

fig, ax = plt.subplots(figsize=(14, 6))
line, = ax.plot(t, harmonic_function(t, initial_parameters['amplitude'],initial_parameters['frequency'],
                    initial_parameters['phase'],initial_parameters['noise_mean'],initial_parameters['noise_covariance'],initial_parameters['show_noise']), lw=2)

fig.subplots_adjust(bottom=0.3)
sliders = {}
param_names = ['Frequency', 'Amplitude', 'Phase', 'Noise mean', 'Noise covariance']
param_keys = ['frequency', 'amplitude', 'phase', 'noise_mean', 'noise_covariance']
param_limits = {'frequency': (0, 10), 'amplitude': (0, 5), 'phase': (0, 2 * np.pi), 'noise_mean': (-1, 1), 'noise_covariance': (0, 1)}
for i in range(4, -1, -1):
    name = param_names[i]
    key = param_keys[i]
    param = initial_parameters[key]
    valmin, valmax = param_limits[key]
    axes = fig.add_axes([0.1, 0.01 + 0.05 * i, 0.65, 0.03])
    sliders[name.lower()] = create_slider(axes, name, valmin, valmax, param)



# # Create checkbutton to toggle noise
ax_noise_toggle = fig.add_axes([0.8, 0.15, 0.1, 0.04])
noise_toggle_button = CheckButtons(ax=ax_noise_toggle, labels=['Show noise'], actives=[initial_parameters['show_noise']])
noise_toggle_button.on_clicked(toggle_noise)
sliders['show_noise'] = noise_toggle_button
# Create a button to reset the sliders to initial values.
ax_reset = fig.add_axes([0.8, 0.025, 0.1, 0.04])
button_reset = Button(ax_reset, 'Reset', hovercolor='0.975')
button_reset.on_clicked(reset)

# Connect sliders to update function
for slider in sliders.values():
    if isinstance(slider, Slider):
        slider.on_changed(update)
    elif isinstance(slider, CheckButtons):
        slider.on_clicked(toggle_noise)

plt.show()