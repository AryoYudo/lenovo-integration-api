import sys
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
        grid_frame.grid_columnconfigure(0, weight=2)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)
        grid_frame.grid_columnconfigure(3, weight=0)
        grid_frame.grid_rowconfigure(0, weight=0)
        # grid_frame.grid_rowconfigure(1, weight=3)

        # Gambar kamera
        self.create_camera_label(grid_frame, 0, 0)

        # Statistik
        self.create_stat_label("GOOD", "1127", "#199C42", grid_frame, 0, 1)
        self.create_stat_label("NG", "110", "#CD202E", grid_frame, 0, 2)
        self.create_stat_label("INPUT", "1237", "#FFB100", grid_frame, 1, 1)    
        self.create_stat_label("YIELD", "95%", "#348CD9", grid_frame, 1, 2)

        # Frame untuk Top 10 Defect Chart
        self.top_defect_frame = tk.Frame(grid_frame, bg="white") 
        self.top_defect_frame.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=10, pady=5)
        self.create_chart(self.top_defect_frame)

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

        title_label = ctk.CTkLabel(frame, text=title, fg_color=color, text_color="white", font=("Arial", 24, "bold"), height=50)
        title_label.pack(fill="x")

        value_label = ctk.CTkLabel(frame, text=value, text_color="black", font=("Arial", 30, "bold"), height=100)
        value_label.pack(fill="both", expand=True, pady=5)

    def create_camera_label(self, parent, row, col):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=5, pady=5)

        framein = ctk.CTkFrame(frame, fg_color="#D3D3D3", corner_radius=10)
        framein.pack(fill="both", expand=True, padx=10, pady=10)

        image_label = ctk.CTkLabel(framein, text="")
        image_label.pack(fill="both", expand=True, pady=10)

        try:
            image = Image.open("images/image.png").resize((250, 250))
            img = ImageTk.PhotoImage(image)
            image_label.configure(image=img)
            image_label.image = img
        except:
            image_label.configure(text="[No Image]")

        text_label = ctk.CTkLabel(framein, text="Camera Inspection", text_color="black", font=("Arial", 18, "bold"))
        text_label.pack(pady=5, fill='both')

    def create_chart(self, parent):
        defects = ["LINE 1", "LINE 2", "LINE 3", "LINE 4", "LINE 5",
                   "LINE 6", "LINE 7", "LINE 8", "LINE 9", "LINE 10"]
        values = [90, 40, 80, 25, 35, 30, 95, 50, 28, 45]

        fig = Figure(figsize=(6, 3.5), dpi=100)
        ax = fig.add_subplot(111)

        ax.barh(defects, values, color="#2ECC71")
        ax.invert_yaxis()
        ax.set_xlabel("Defect Count")
        ax.set_title("Top 10 Defects", fontsize=14, fontweight='bold')

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)

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
