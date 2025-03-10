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
        self.init_title_bar(main_frame)

        # Grid Layout
        grid_frame = ctk.CTkFrame(main_frame)
        grid_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Konfigurasi grid
        grid_frame.grid_columnconfigure(0, weight=2)
        grid_frame.grid_columnconfigure(1, weight=1)
        grid_frame.grid_columnconfigure(2, weight=1)
        grid_frame.grid_columnconfigure(3, weight=0)

        grid_frame.grid_rowconfigure(0, weight=1, minsize=200)
        grid_frame.grid_rowconfigure(1, weight=0)
        grid_frame.grid_rowconfigure(2, weight=3)  # Menambahkan row untuk tabel
        grid_frame.grid_propagate(False)

        # Gambar kamera
        self.create_camera_label(grid_frame, 0, 0)

        # Statistik
        self.create_stat_label("GOOD", "1127", "#199C42", grid_frame, 0, 1)
        self.create_stat_label("NG", "110", "#CD202E", grid_frame, 0, 2)
        self.create_stat_label("INPUT", "1237", "#FFB100", grid_frame, 1, 1)
        self.create_stat_label("YIELD", "95%", "#348CD9", grid_frame, 1, 2)

        # Frame untuk Top 10 Defect Chart
        self.top_defect_frame = tk.Frame(grid_frame, bg="white")
        self.top_defect_frame.grid(row=0, column=3, rowspan=2, sticky="nsew", padx=5, pady=5)
        self.create_chart(self.top_defect_frame)

        # Table Widget - Dipindahkan ke row 2
        self.create_table(grid_frame, 2, 0)
        self.result_inspection_camera(grid_frame, 2, 1)
    def init_title_bar(self, parent):
        """Membuat header seperti title bar kustom"""
        title_bar = ctk.CTkFrame(parent, fg_color="#d32f2f", height=40, corner_radius=0)
        title_bar.pack(fill="x")

        # Label judul
        title_label = ctk.CTkLabel(title_bar, text="AOI - SOLDER INSPECTION V.1.0",
                                   text_color="white", font=("Arial", 14, "bold"))
        title_label.pack(side="left", padx=10)

        # Tombol close
        close_btn = ctk.CTkButton(title_bar, text="✕", width=30, fg_color="#b71c1c", text_color="white",
                                  command=self.quit)
        close_btn.pack(side="right", padx=5)
         # Tombol fullscreen toggle
         
        self.is_fullscreen = False  # Status fullscreen
        
        def toggle_fullscreen():
            self.is_fullscreen = not self.is_fullscreen
            self.attributes("-fullscreen", self.is_fullscreen)
        
        fullscreen_btn = ctk.CTkButton(title_bar, text="⛶", width=30, fg_color="#b71c1c", text_color="white",
                                    command=toggle_fullscreen)
        fullscreen_btn.pack(side="right", padx=5)

        # Tombol minimize
        minimize_btn = ctk.CTkButton(title_bar, text="—", width=30, fg_color="#b71c1c", text_color="white",
                                     command=self.iconify)
        minimize_btn.pack(side="right", padx=5)


        # Event untuk drag window
        title_bar.bind("<ButtonPress-1>", self.start_move)
        title_bar.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        """Menyimpan posisi awal saat window di-drag"""
        self.x = event.x_root
        self.y = event.y_root

    def on_move(self, event):
        """Memindahkan window saat di-drag"""
        dx = event.x_root - self.x
        dy = event.y_root - self.y
        self.geometry(f"+{self.winfo_x() + dx}+{self.winfo_y() + dy}")
        self.x = event.x_root
        self.y = event.y_root

    def create_stat_label(self, title, value, color, parent, row, col):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

        title_label = ctk.CTkLabel(frame, text=title, fg_color=color, text_color="white", font=("Arial", 24, "bold"), height=50)
        title_label.pack(fill="x")

        value_label = ctk.CTkLabel(frame, text=value, text_color="black", font=("Arial", 40, "bold"), height=150)
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

    def create_table(self, parent, row, col):
        """ Membuat tabel dengan header, isi, dan footer """
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=row, column=col, sticky="nsew", padx=5, pady=5, columnspan=1)

        # Konfigurasi frame agar tidak menyusut
        frame.grid_propagate(False)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(1, weight=1)  # Memberi ruang ke isi tabel

        # Header tabel
        headers = ["Component", "Part Number", "Defect Description"]
        header_frame = ctk.CTkFrame(frame, fg_color="#CED3D7")
        header_frame.pack(fill="x", padx=5, pady=2)

        for col, text in enumerate(headers):
            ctk.CTkLabel(header_frame, text=text, width=200, anchor="w", font=("Arial", 12, "bold"))\
                .pack(side="left", padx=5, pady=5)

        # Data isi tabel
        data = [
            ("PCB-REELID", "PN-1234", "Short Circuit"),
            ("Resistor", "PN-5678", "Solder Ball"),
            ("Capacitor", "PN-9101", "Open Solder"),
            ("IC Chip", "PN-1123", "Misalignment"),
            ("Connector", "PN-1415", "Missing Component"),
            ("Diode", "PN-1617", "Tombstone")
        ]

        # Isi tabel
        table_content = ctk.CTkFrame(frame, fg_color="white")
        table_content.pack(fill="both", expand=True, padx=5, pady=2)

        for part, num, defect in data:
            row_frame = ctk.CTkFrame(table_content, fg_color="#EBEBEB")
            row_frame.pack(fill="x", padx=5, pady=1)

            ctk.CTkLabel(row_frame, text=part, width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=num, width=200, anchor="w").pack(side="left", padx=5)
            ctk.CTkLabel(row_frame, text=defect, width=250, anchor="w").pack(side="left", padx=5)

        # Footer di dalam tabel
        footer = ctk.CTkLabel(frame, text="NG", fg_color="red", text_color="white",
                              font=("Arial", 20, "bold"), height=40)
        footer.pack(side="bottom", fill="x", padx=5, pady=5)
    
    def result_inspection_camera(self, parent, row, col):
        frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=10)
        frame.grid(row=row, column=col, rowspan=2, sticky="nsew", padx=5, pady=5, columnspan=3)

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


if __name__ == '__main__':
    ctk.set_appearance_mode("light")
    app = SolderInspectionApp()
    app.mainloop()