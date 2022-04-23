import time
import numpy as np
from random import randint
import galois
import math

class Eliptic_curve_point:
    def __init__(self, point, pointer, point_ord, points):
        self.point = point
        self.point_ord = point_ord
        self.k_points = points
        self.pointer = pointer

    def find_order_of_point(self):
        if self.point["x"] != 0 or self.point["y"] != 0:
            orders = findDivisors(self.pointer.get_Order())
            nas = 1
            k = []
            k.append(nas)
            k.append(self.point)
            self.k_points.append(k)
            for ind in orders:
                if ind == 1:
                    continue
                while nas + nas <= ind:
                    k = []
                    nas = nas + nas
                    k.append(nas)
                    k.append(self.pointer.sum_points(self.k_points[-1][1], self.k_points[-1][1]))
                    self.k_points.append(k)
                if self.k_point(ind) == {"x":self.pointer.GF(0), "y":self.pointer.GF(0)}:
                    self.point_ord = ind
                    break

    def k_point(self, stop):
        if self.point_ord < 0 and self.k_points == []:
            self.find_order_of_point()
        if self.point_ord >= 0:
            stop = stop%self.point_ord
        nas = 0
        res = {}
        while nas < stop:
            for i in range(len(self.k_points)):
                if nas + self.k_points[- i - 1][0] <= stop:
                    if not nas:
                        res = self.k_points[- i - 1][1]
                        nas += self.k_points[- i - 1][0]
                        continue
                    res = self.pointer.sum_points(res, self.k_points[- i - 1][1])
                    nas += self.k_points[- i - 1][0]
        return res

class Eliptic_curve_coding:
    def __init__(self, GF, a, b, pointer=0):
        self.GF = GF
        self.a = self.GF(a)
        self.b = self.GF(b)
        self.points = []
        self.order = 0
        self.pointer = pointer
        self.message = []

    def setPointer(self, value):
        self.pointer = value

    def get_Order(self):
        return self.order

    def check_discr(self):
        if 4*self.a**3+27*self.b**2 != 0:
            return True
        return False

    def y_points_elip_curve(self):
        if self.check_discr():
            value_x= np.empty(self.GF.characteristic, dtype=np.int16)
            value_y= np.empty(self.GF.characteristic, dtype=np.int16)
            p = galois.Poly([1,0,self.a,self.b], field=self.GF)
            for i in range(self.GF.characteristic):
                value_x[i] = p(i)
                value_y[i] = i**2%self.GF.characteristic

            for i in range(self.GF.characteristic):
                if value_x[i] in value_y:
                    for j in range(self.GF.characteristic):
                        if value_x[i] == value_y[j]:
                            point = {}
                            point['x'] = self.GF(i)
                            point['y'] = self.GF(j)
                            self.points.append(point)
            self.order = len(self.points)+1
            self.points = np.asarray(self.points, dtype = object)
        else:
            return "Není eliptická křivka nevyšel diskriminant."

    def sum_points(self, first, second):
        point = {}
        if second["x"] - first["x"] == 0:
            if first == second:
                if first["y"] != 0:
                    point["x"] = ((3 * first["x"]**2 + self.a) / (2 * first["y"]))**2 - 2 * first["x"]
                    point["y"] = ((3 * first["x"]**2 + self.a) / (2 * first["y"])) * (first["x"] - point["x"]) - first["y"]
                else:
                    point["x"] = self.GF(0)
                    point["y"] = self.GF(0)
            else:
                point["x"] = self.GF(0)
                point["y"] = self.GF(0)
        else:
            point["x"] = ((second["y"] - first["y"]) / (second["x"]-first["x"]))**2 - first["x"] - second["x"]
            point["y"] = ((second["y"] - first["y"]) / (second["x"]-first["x"])) * (first["x"] - point["x"]) - first["y"]
        return point

    def encoding(self, ind_point, k, m):
        P = Eliptic_curve_point(self.points[ind_point], self.pointer, -1 ,[])
        P.find_order_of_point()
        Q = Eliptic_curve_point(P.k_point(k), self.pointer, -1 ,[])
        a = randint(0, self.order)
        points = {}
        points["C1"] = Eliptic_curve_point(P.k_point(a), self.pointer, -1 ,[])
        mess = np.empty(len(m), dtype=object)
        for ch in range(len(m)):
            mess[ch] = self.sum_points(self.points[ord(m[ch])], Q.k_point(a))
        points["C2"] = mess
        return points

    def decoding(self, mess, k):
        message = ""
        for i in range(len(mess["C2"])):
            point = self.subtraction(mess["C2"][i], mess["C1"].k_point(k))
            message = message + chr(np.where(self.points == point)[0][0])
        print(f"\nDekódovaná zpráva je: start|\n{message}\n|konec")
        return message

    def subtraction(self, f,s):
        s["y"] = -s["y"]
        return self.sum_points(f,s)

def findDivisors(n):
    i = 1
    value = []
    while i <= math.sqrt(n):
        if (n % i == 0):
            if (n / i == i) :
                value.append(i)
            else :
                value.append(i)
                value.append(int(n/i))
        i = i + 1
    value.sort()
    return value

def start():
    gal = input("Zadejte velikost Galois field: ")
    a = input("Zadejte a koeficient: ")
    b = input("Zadejte b koeficient: ")
    tic = time.perf_counter()
    gf = galois.GF(int(gal))
    curve = Eliptic_curve_coding(gf, int(a), int(b))
    curve.setPointer(curve)
    p = curve.y_points_elip_curve()  
    toc = time.perf_counter() 
    ti = toc - tic
    k = int(input("Zadejte secret key k koeficient: "))
    env = input(f"Chcete zvolit P náhodně zadejte 'y': pokud ne zadejte číslo <0;{curve.order-2}> Pozn: (inf bod je vynechán): ")
    if env == "y":
        P = randint(0, curve.order)
    else:
        P = int(env)
    print("Pozn. pro použití na češtinu je potřeba aby GF mělo aspoň 500 bodů vzhledem ke způsobu přiřazování \nideální je se řídít podle UTF-8 stanadardu, tudiž pro češtinu potřebujeme 2 bajty = 1920 znaků/bodů")
    inp = input("Zadejte text co chcete zakódovat: start|\n")
    print("|konec")
    tic = time.perf_counter()
    message = curve.decoding(curve.encoding(P, k, inp), k)
    toc = time.perf_counter()
    return ti + toc - tic

def createElipCurve(gal, a, b):
    gf = galois.GF(int(gal))
    curve = Eliptic_curve_coding(gf, int(a), int(b))
    curve.setPointer(curve)
    p = curve.y_points_elip_curve()  
    return curve

def encode(curve, k, m, ind):
    return curve.encoding(ind, k, m)

def decode(curve, point, k):
    return curve.decoding(point, k)