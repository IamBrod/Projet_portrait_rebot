import interfacegraphique
import customtkinter as ctk


ctk.set_appearance_mode("light")   
ctk.set_default_color_theme("blue")
root = ctk.CTk()
interfacegraphique.PortraitRobotApp(root)
root.mainloop()