from tkinter import *
from tkinter import messagebox
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

root = Tk()
root.title("Thuật toán A*")
root.resizable(height=True, width=True)
root.minsize(height=600, width= 600)
root["bg"] = "grey"

# màn hình ở giữa
def makeCenter(root):
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth()//2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x,y))

makeCenter(root)

# tìm các phần tử nằm trên đường đi
def road(startElement, lastElement, father):
  way = []
  edge = []
  way.append(lastElement)
  while len(way) != 0:
    # pop an element
    item = way.pop()
    if father[item] == startElement:
      edge.append(tuple((father[item], item)))
      way.append(item)
      way.append(father[item])
      break
    else:
      edge.append(tuple((father[item], item)))
      way.append(item)
      way.append(father[item])

  return way[::-1], edge
# đóng đồ thị
def plt_close():
    plt.close()

# hiển thị đồ thị
def draw_grap(father, way, edge):
    # Tạo một đối tượng đồ thị có hướng
    G = nx.DiGraph()

    # Thêm các nút vào đồ thị (chúng ta sẽ sử dụng số nguyên làm nút)
    nodes = list(set(list(father.keys()) + list(father.values())))
    G.add_nodes_from(nodes)

    # Thêm các cạnh cho cây đồ thị nhị phân (các cạnh có hướng từ cha đến con)
    edges= []
    for key,value in father.items():
        edges.append(tuple((value, key)))
    G.add_edges_from(edges)

    # Sắp xếp nút tự động với thuật toán kamada_kawai_layout
   # pos = nx.kamada_kawai_layout(G)

    # Đặt màu cho một số nút
    node_colors = ["indianred" if node in way else "cornflowerblue" for node in G.nodes]

    # Đặt màu cho một số mũi tên (cạnh)
    edge_colors = ["red" if item in edge else "black" for item in G.edges]

    # Vẽ đồ thị với mũi tên từ cha đến con
    nx.draw(G, with_labels=True, node_size=500, node_color=node_colors, edge_color=edge_colors, arrows=True)
    plt.show()

# Thuật toán A*
class List:
  def __init__(self):
    self.__vertex = []

  # check empty
  def empty_list(self):
    return len(self.__vertex) == 0

  # push element
  def push(self, a):
    self.__vertex.append(a)
    self.__vertex.sort(key = lambda x:x[1])

  # pop element
  def pop(self):
    return self.__vertex.pop(0)

  def print(self):
    print(self.__vertex)

# hàm A*
def A_sao(matrix, start_element, last_element, list_vertex):
  vertex = List()
  # push the start element
  vertex.push(tuple((start_element, 0)))

  # father to store father of all element
  father  = {}

  # check vertex
  check_vertex = np.zeros(shape = len(matrix), dtype = int)
  check_vertex[start_element] = 1

  Gv = {}
  while vertex.empty_list() == False:
    item = vertex.pop()
    if item[0] in last_element:
        plt_close()
        way, edge =  road(list_vertex[start_element], list_vertex[item[0]], father)
        draw_grap(father,way, edge)
        return

    if item[0] == start_element:
      for i in range(len(matrix)):
        if (matrix[item[0]][i][0] > -1) and (check_vertex[i] == 0):
          check_vertex[i] = 1
          father.setdefault(list_vertex[i], list_vertex[item[0]])
          Gv.setdefault(i, matrix[item[0]][i][0])
          Fv = Gv[i] + matrix[item[0]][i][1]
          vertex.push(tuple((i, Fv)))
    else:
      for i in range(len(matrix)):
        if (matrix[item[0]][i][0] > -1) and (check_vertex[i] == 0):
          check_vertex[i] = 1
          father.setdefault(list_vertex[i], list_vertex[item[0]])
          Gv.setdefault(i, Gv[item[0]]+matrix[item[0]][i][0])
          Fv = Gv[i] + matrix[item[0]][i][1]
          vertex.push(tuple((i, Fv)))

  last_element = [list_vertex[x] for x in last_element]
  messagebox.showinfo("Thông báo", f"không tồn tại đường đi từ đỉnh {list_vertex[start_element]} đến {last_element}")

# các hàm
# xóa các thành phần khi nhấn 2 lần button Giải
def del_thanh_phan(thanh_phan):
    for item in thanh_phan.winfo_children()[1:]:
        item.destroy()

def mo_phong(ten_dinh, matrix, dinh_bat_dau, dinh_ket_thuc):
    ten_dinh = [x.get().strip() for x in ten_dinh]
    print("tên đỉnh:", ten_dinh)
    # kiểm tra đỉnh bắt đầu có tồn tại hay không?
    if dinh_bat_dau.get().strip() in ten_dinh:
        dinh_bat_dau = dinh_bat_dau.get().strip()
    else:
        messagebox.showinfo("Thông báo", "Đỉnh bắt đầu không tồn tại! vui lòng nhập lại")
        return

    dinh_ket_thuc = dinh_ket_thuc.get().strip().replace(" ", "")
    dinh_ket_thuc = dinh_ket_thuc.split(",")
    # kiểm tra đỉnh kết thúc có tồn tại hay không
    if all(item in ten_dinh for item in dinh_ket_thuc) == False:
        messagebox.showinfo("Thông báo", "Đỉnh kết thúc không tồn tại! vui lòng nhập lại")
        return

    matrixA = []
    for line in matrix:
        lineA = []
        for item in line:
            try:
                item = item.get().strip().replace(" ", "")
                lineA.append(tuple((map(lambda x : float(x), item.split("|")))))
            except Exception:
                messagebox.showinfo("Thông báo","Bạn nhập kiểu dữ liệu của ma trận không đúng!, hãy nhập kiểu dữ liệu số.")
                return
        matrixA.append(lineA)

    index_dinh_ket_thuc = []
    for i in dinh_ket_thuc:
        index_dinh_ket_thuc.append(ten_dinh.index(i))

    A_sao(matrixA, ten_dinh.index(dinh_bat_dau), index_dinh_ket_thuc, ten_dinh)

def them_thanh_phan(thanh_phan, so_dinh):
    ten_dinh = []
    matrix = []
    dinh_bat_dau = StringVar()
    dinh_ket_thuc = StringVar()

    # thêm đỉnh bắt đầu
    dinh_start = Frame(thanh_phan)
    Label(dinh_start, text="Đỉnh bắt đầu:", justify=RIGHT).pack(side=LEFT)
    Entry(dinh_start, width=20, textvariable=dinh_bat_dau, borderwidth=5).pack(side=LEFT)
    dinh_start.grid(row=2, column=0)

    # thêm đỉnh kết thúc
    dinh_final = Frame(thanh_phan)
    Label(dinh_final, text="Đỉnh cuối:", padx = 10,justify=RIGHT).pack(side=LEFT)
    Entry(dinh_final, width=20, textvariable=dinh_ket_thuc, borderwidth=5).pack(side=LEFT)
    dinh_final.grid(row=3, column=0)

    # tên đỉnh
    item_ten_dinh = Frame(thanh_phan)
    Label(item_ten_dinh, text="Tên đỉnh:").pack(side=LEFT, padx=3)
    for i in range(so_dinh):
        string_item = StringVar()
        Entry(item_ten_dinh, width=5, borderwidth=5, textvariable=string_item).pack(side=LEFT, padx=3)
        ten_dinh.append(string_item)
    item_ten_dinh.grid(row=4, column=0, pady=10)

    # ma trận đỉnh
    Label(thanh_phan, text="Ma trận:", justify=LEFT).grid(row=5, column=0)
    for i in range(so_dinh):
        line_matrix = []
        item_in_thanh_phan = Frame(thanh_phan)
        for j in range(so_dinh):
            string_item = StringVar()
            Entry(item_in_thanh_phan, width=5, borderwidth=5, textvariable=string_item).pack(side=LEFT, padx=3)
            line_matrix.append(string_item)
        item_in_thanh_phan.grid(row=i+6, column=0)
        matrix.append(line_matrix)

    # button mô phỏng và thoát
    button_moPhong_thoat = Frame(thanh_phan)
    Button(button_moPhong_thoat, text="Mô phỏng", bg="indianred", command= lambda : mo_phong(ten_dinh, matrix, dinh_bat_dau, dinh_ket_thuc)).pack(side=LEFT)
    Button(button_moPhong_thoat, text="Thoát", bg = "indianred", command=lambda :del_thanh_phan(thanh_phan)).pack(side=LEFT)
    button_moPhong_thoat.grid(row=so_dinh+6, column=0)

    Label(thanh_phan, text="chú ý: nhập ma trận dưới dạng {k(u,v)|g(x)}").grid(row=so_dinh +7, column=0)
    Label(thanh_phan, text="").grid(row=so_dinh+8, column=0)

def button_giai(thanh_phan, stringSoDinh):
    if stringSoDinh.get() == "":
        messagebox.showinfo("Thông báo","Bạn chưa nhập số đỉnh")
        return
    else:
        try:
            del_thanh_phan(thanh_phan)
            them_thanh_phan(thanh_phan, int(stringSoDinh.get()))
        except Exception:
            messagebox.showinfo("Thông báo", "Hãy nhập kiểu dữ liệu số cho số đỉnh!")
            return
# thêm các thành phần
# thêm tiêu đề
label = Label(root, text="Mô Phỏng Thuật Toán A*", bg="yellow", font=("tahoma", 20), justify=CENTER, width=40)
label.grid(row=0, column=0, pady=10)
# thêm số đỉnh
stringSoDinh = StringVar()
thanh_phan = Frame(root, width=40)
# nhãn quan trọng
lbl_import = Frame(thanh_phan)
Label(lbl_import, text= "Số đỉnh:", font=("arial", 11, "bold")).pack(side=LEFT, padx=3)
Entry(lbl_import, width= 20,borderwidth=5, textvariable=stringSoDinh).pack(side=LEFT, padx=3)
Button(lbl_import, text="Giải", background="indianred", width=6, command=lambda :button_giai(thanh_phan, stringSoDinh)).pack(side=LEFT, padx=3)
lbl_import.grid(row=0, column=0, pady=5)
thanh_phan.grid(row=1, column=0)
root.mainloop()
