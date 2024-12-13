import tkinter as tk
from tkinter import ttk
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL


def get_default_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    return volume.GetMasterVolumeLevelScalar()


def set_volume(level):
    level = float(level)
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMasterVolumeLevelScalar(level, None)  # Volume entre 0.0 e 1.0
    print(f"Volume definido para {int(level * 100)}%")


def mute_volume(mute=True):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    volume.SetMute(1 if mute else 0, None)
    print("Som mutado" if mute else "Som ativado")


def toggle_mute(channel_index, slider_value, button):
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = interface.QueryInterface(IAudioEndpointVolume)
    current_volume = volume.GetChannelVolumeLevelScalar(channel_index)  # Volume atual do canal

    if current_volume == 0.0:
        # Desmuta e ajusta o volume com base no slider
        volume.SetChannelVolumeLevelScalar(channel_index, float(slider_value), None)
        button.config(text=f"Mutar")
        print(f"Canal {channel_index} desmutado e volume ajustado para {slider_value}.")
    else:
        # Muta o canal
        volume.SetChannelVolumeLevelScalar(channel_index, 0.0, None)
        button.config(text=f"Desmutar")
        print(f"Canal {channel_index} mutado.")


# Criação de interface
class VolumeMixerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Volume")

        default_volume = get_default_volume()

        # volume geral
        self.volume_label = ttk.Label(root, text="Volume Geral:")
        self.volume_label.pack(pady=10)

        self.volume_slider = ttk.Scale(root, from_=0.0, to=1.0, orient="horizontal", command=self.update_volume)
        self.volume_slider.set(default_volume)
        self.volume_slider.pack(pady=10)

        # botao para mutar esquerdo
        self.mute_left_label = ttk.Label(root, text="Esquerdo")
        self.mute_left_label.pack(pady=10)
        self.mute_left_btn = ttk.Button(root, text="Mutar",
                                        command=lambda: toggle_mute(1, self.volume_slider.get(), self.mute_left_btn))
        self.mute_left_btn.pack(pady=5)

        # direito
        self.mute_right_label = ttk.Label(root, text="Direito")
        self.mute_right_label.pack(pady=10)
        self.mute_right_btn = ttk.Button(root, text="Mutar",
                                         command=lambda: toggle_mute(0, self.volume_slider.get(), self.mute_right_btn))
        self.mute_right_btn.pack(pady=5)

    def update_volume(self, value):
        set_volume(value)


if __name__ == "__main__":
    root = tk.Tk()
    app = VolumeMixerApp(root)
    root.mainloop()
