import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

class SolderInspectionApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.title("AOI - SOLDER INSPECTION V.1.0")
        self.attributes('-fullscreen', True)

        main_frame = ctk.CTkFrame(self)
        main_frame.pack(fill="both", expand=True)

        # Header
        header = ctk.CTkLabel(main_frame, text="AOI - SOLDER INSPECTION V.1.0", fg_color="#d32f2f", text_color="white", font=("Arial", 20, "bold"), height=40)
        header.pack(fill="x")

        # Grid Layout untuk elemen utama
        grid_frame = ctk.CTkFrame(main_frame)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        grid_frame.grid_columnconfigure((0, 1, 2, 3), weight=10)
        grid_frame.grid_rowconfigure((0, 1), weight=109)

        # Gambar kamera
        self.create_camera_label(grid_frame, 1, 0)

        # Statistik
        self.create_stat_label("GOOD", "1127", "#199C42", grid_frame, 0, 1)
        self.create_stat_label("NG", "110", "#CD202E", grid_frame, 0, 2)
        self.create_stat_label("INPUT", "1237", "#FFB100", grid_frame, 1, 1)
        self.create_stat_label("YIELD", "95%", "#348CD9", grid_frame, 1, 2)

        # Label Top Defect
        self.top_defect_label = tk.Label( grid_frame, text="TOP 10 DEFECT", bg="white", fg="black", font=("Arial", 16, "bold"), height=20, anchor="n" )
        self.top_defect_label.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=10, pady=5)

        # Table Widget
        self.table = ctk.CTkFrame(main_frame)
        self.table.pack(fill="both", expand=True, padx=10, pady=10)
        self.fill_table()

        # Footer
        footer = ctk.CTkLabel(main_frame, text="NG", fg_color="red", text_color="white", font=("Arial", 20, "bold"), height=40)
        footer.pack(fill="x")

    def create_stat_label(self, title, value, color, parent, row, col):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        title_label = ctk.CTkLabel(frame, text=title, fg_color=color, text_color="white", font=("Arial", 28, "bold"), height=40)
        title_label.pack(fill="x")

        value_label = ctk.CTkLabel(frame, text=value, fg_color="white", text_color="black", font=("Arial", 24, "bold"), height=150)
        value_label.pack(fill="both", expand=True, pady=5)

    def create_camera_label(self, parent, row, col):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=5, pady=5)

        image_label = ctk.CTkLabel(frame, text="")
        image_label.pack()
        try:
            image = Image.open("images/image.png").resize((180, 180))
            img = ImageTk.PhotoImage(image)
            image_label.configure(image=img)
            image_label.image = img
        except:
            image_label.configure(text="[No Image]")

        text_label = ctk.CTkLabel(frame, text="Camera Ianspection", text_color="black", font=("Arial", 32, "bold"))
        text_label.pack()

    def fill_table(self):
        data = [
            ("PCB-REELID", "PN-1234", "Short Circuit"),
            ("Resistor", "PN-5678", "Solder Ball"),
            ("Capacitor", "PN-9101", "Open Solder"),
            ("IC Chip", "PN-1123", "Misalignment"),
            ("Connector", "PN-1415", "Missing Component"),
            ("Diode", "PN-1617", "Tombstone")
        ]
        
        for row, (part, num, defect) in enumerate(data):
            row_frame = ctk.CTkFrame(self.table, fg_color="white", corner_radius=5)
            row_frame.pack(fill="x", padx=5, pady=2)
            
            ctk.CTkLabel(row_frame, text=part, width=120, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=num, width=100, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=defect, width=150, anchor="w").pack(side="left", padx=5)

if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    app = SolderInspectionApp()
    app.mainloop()