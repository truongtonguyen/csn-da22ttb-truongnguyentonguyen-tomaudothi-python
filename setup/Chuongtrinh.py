import tkinter as tk
from tkinter import messagebox
import random
import time

class Dothi:
    def __init__(self):
        self.V = 0  # Số đỉnh
        self.dothi = {}  # Đồ thị rỗng

    def them_dinh(self):
        self.dothi[self.V] = []
        self.V += 1

    def them_canh(self, u, v):
        self.dothi[u].append(v)
        self.dothi[v].append(u)

    def ma_tran_ke(self, matran):
        self.V = len(matran)
        self.dothi = {i: [] for i in range(self.V)}
        for i in range(self.V):
            for j in range(self.V):
                if matran[i][j] == 1:
                    self.dothi[i].append(j)
                    self.dothi[j].append(i)

    def Welch_Powell(self):
        dinh_theo_bac_giam_dan = sorted(self.dothi.keys(),
                                         key = lambda u : len(self.dothi[u]), reverse= True)
        ketqua = [-1] * self.V

        for u in dinh_theo_bac_giam_dan:
            mau_da_dung = set()
            for v in self.dothi[u]:
                if ketqua[v] != -1:
                    mau_da_dung.add(ketqua[v])

            mau = 0
            while mau in mau_da_dung:
                mau +=1
            ketqua[u] = mau

        return ketqua

    def Backtracking(self, mau_toi_da):
        ketqua = [-1] * self.V

        def thu(u, mau):
            for v in self.dothi[u]:
                if ketqua[v] == mau:
                    return False
            return True

        def quay_lai(u):
            if u == self.V:
                return True

            for mau in range(mau_toi_da):
                if thu(u, mau):
                    ketqua[u] = mau
                    if quay_lai(u + 1):
                        return True
                    ketqua[u] = -1

            return False

        for mau_toi_da in range(1, mau_toi_da + 1):
            if quay_lai(0):
                return ketqua

        return ketqua  # Trả về kết quả dù không tìm được với số màu tối ưu

class Tomau:
    def __init__(self, root):
        self.root = root
        self.root.title("Giải thuật tô màu đồ thị")
        self.root.geometry("800x600")

        self.dothi = Dothi()
        self.dinh = []
        self.canh = []

        # Giao diện nhập liệu
        self.khung = tk.Frame(root)
        self.khung.pack(pady=10)

        # Nút chọn cách nhập
        tk.Button(self.khung, text="Thêm Đỉnh và Cạnh Thủ Công",
                   command=self.che_do_thu_cong).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(self.khung, text="Nhập Ma Trận Kề",
                   command=self.che_do_ma_tran_ke).grid(row=0, column=1, padx=5, pady=5)

        # Nút vẽ và tô màu đồ thị
        tk.Button(self.khung, text="Vẽ Đồ Thị",
                   command=self.ve_do_thi).grid(row=0, column=2, padx=5, pady=5)
        tk.Button(self.khung, text="Tô Màu (Welch-Powell)",
                   command=self.to_mau_Welch_Powell).grid(row=0, column=3, padx=5, pady=5)
        tk.Button(self.khung, text="Tô Màu (Backtracking)",
                   command=self.to_mau_Backtracking).grid(row=0, column=4, padx=5, pady=5)

        self.bao_kq = tk.Label(root, text="")
        self.bao_kq.pack(pady=10)

        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(pady=10)

    def che_do_thu_cong(self):
        self.giao_dien_thu_cong = tk.Toplevel(self.root)
        self.giao_dien_thu_cong.title("Nhập Thủ Công")

        # Nút thêm đỉnh
        tk.Button(self.giao_dien_thu_cong, text="Thêm Đỉnh",
                   command=self.them_dinh).pack(pady=5)
        
        # Nhập cạnh
        tk.Label(self.giao_dien_thu_cong, text="Thêm cạnh (u, v):").pack(pady=5)
        self.nhap_dinh_u = tk.Entry(self.giao_dien_thu_cong, width=5)
        self.nhap_dinh_u.pack(side=tk.LEFT, padx=5)
        self.nhap_dinh_v = tk.Entry(self.giao_dien_thu_cong, width=5)
        self.nhap_dinh_v.pack(side=tk.LEFT, padx=5)
        tk.Button(self.giao_dien_thu_cong, text="Thêm Cạnh",
                   command=self.them_canh).pack(side=tk.LEFT, padx=5)
        
    def them_dinh(self):
        self.dothi.them_dinh()
        self.dinh.append((random.randint(50, 550), random.randint(50, 350)))
        messagebox.showinfo("Thông Báo", f"Đã thêm đỉnh {self.dothi.V - 1}.")

    def them_canh(self):
        try:
            u = int(self.nhap_dinh_u.get())
            v = int(self.nhap_dinh_v.get())
            if u < 0 or v < 0 or u >= self.dothi.V or v >= self.dothi.V:
                raise ValueError("Đỉnh không hợp lệ!")
            self.dothi.them_canh(u, v)
            self.canh.append((u, v))
            messagebox.showinfo("Thông Báo", f"Đã thêm cạnh ({u}, {v}).")
        except ValueError as e:
            messagebox.showerror("Lỗi", str(e))

    def che_do_ma_tran_ke(self):
        self.giao_dien_ma_tran = tk.Toplevel(self.root)
        self.giao_dien_ma_tran.title("Nhập Ma Trận Kề")
        tk.Label(self.giao_dien_ma_tran, text="Nhập ma trận kề:").pack(pady=10)
        self.khung_ma_tran = tk.Text(self.giao_dien_ma_tran, width=50, height=10)
        self.khung_ma_tran.pack(pady=5)

        tk.Button(self.giao_dien_ma_tran, text="Xác Nhận",
                   command=self.do_thi_tu_ma_tran).pack(pady=5)

    def do_thi_tu_ma_tran(self):
        try:
            ma_tran_da_nhap = self.khung_ma_tran.get("1.0", tk.END).strip()
            matran = [[int(x) for x in row.split()] for row in ma_tran_da_nhap.split("\n")]

            if not all(len(row) == len(matran) for row in matran):
                raise ValueError("Ma trận kề phải là ma trận vuông!")

            self.dothi.ma_tran_ke(matran)
            self.dinh = self.ds_dinh()
            self.canh = self.ds_canh()
            self.giao_dien_ma_tran.destroy()
            messagebox.showinfo("Thông Báo", "Nhập ma trận kề thành công!")
        except ValueError as e:
            messagebox.showerror("Lỗi", f"Lỗi khi nhập ma trận kề: {str(e)}")
        except Exception:
            messagebox.showerror("Lỗi", "Vui lòng nhập đúng định dạng ma trận kề!")

    def ds_dinh(self):
        dinh = []
        for i in range(self.dothi.V):
            x = random.randint(50, 550)
            y = random.randint(50, 350)
            dinh.append((x, y))
        return dinh

    def ds_canh(self):
        canh = []
        for u in self.dothi.dothi:
            for v in self.dothi.dothi[u]:
                if u < v:  # Đảm bảo không tạo lại cạnh (u, v) và (v, u)
                    canh.append((u, v))
        return canh

    def ve_do_thi(self):
        if self.dothi.V == 0:
            messagebox.showerror("Lỗi", "Hãy nhập đồ thị trước!")
            return

        self.canvas.delete("all")

        # Vẽ các đỉnh
        for i, (x, y) in enumerate(self.dinh):
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill="white", outline="black")
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

        # Vẽ các cạnh
        for u, v in self.canh:
            x1, y1 = self.dinh[u]
            x2, y2 = self.dinh[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

    def to_mau_Welch_Powell(self):
        if self.dothi.V == 0:
            messagebox.showerror("Lỗi", "Hãy nhập đồ thị trước!")
            return

        ds_mau = ["red", "blue", "green", "yellow", "orange", "purple", "pink"]
        tg_bat_dau = time.time()
        ketqua = self.dothi.Welch_Powell()
        tg_ket_thuc = time.time()

        self.ve_khi_to(ketqua, ds_mau)
        thoi_gian = tg_ket_thuc - tg_bat_dau
        so_luong_mau = max(ketqua) + 1

        self.bao_kq.config(text=f"Welch-Powell: {so_luong_mau} màu, {thoi_gian:.5f} giây")
        messagebox.showinfo("Thông Báo", 
                            f"Tô màu Welch-Powell có sắc số: {so_luong_mau}. Thời gian: {thoi_gian:.5f} giây.")

    def to_mau_Backtracking(self):
        if self.dothi.V == 0:
            messagebox.showerror("Lỗi", "Hãy nhập đồ thị trước!")
            return

        ds_mau = ["red", "blue", "green", "yellow", "orange", "purple", "pink"]
        tg_bat_dau = time.time()
        ketqua = self.dothi.Backtracking(len(ds_mau))
        tg_ket_thuc = time.time()

        self.ve_khi_to(ketqua, ds_mau)
        thoi_gian = tg_ket_thuc - tg_bat_dau
        so_luong_mau = max(ketqua) + 1

        self.bao_kq.config(text=f"Backtracking: {so_luong_mau} màu, {thoi_gian:.5f} giây")
        messagebox.showinfo("Thông Báo",
                             f"Tô màu Backtracking có sắc số: {so_luong_mau}. Thời gian: {thoi_gian:.5f} giây.")
        
    def ve_khi_to(self, ketqua, ds_mau):
        self.canvas.delete("all")

        for i, (x, y) in enumerate(self.dinh):
            self.canvas.create_oval(x-15, y-15, x+15, y+15, fill=ds_mau[ketqua[i]], outline="black")
            self.canvas.create_text(x, y, text=str(i), font=("Arial", 12, "bold"))

        for u, v in self.canh:
            x1, y1 = self.dinh[u]
            x2, y2 = self.dinh[v]
            self.canvas.create_line(x1, y1, x2, y2, width=2)

root = tk.Tk()
app = Tomau(root)
root.mainloop()
