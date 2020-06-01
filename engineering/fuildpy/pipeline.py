# mfpy.py - pipeline.py
# v. 0.0.1

import numpy as np
from mfpy import utilities as util
from scipy.optimize import fsolve

# Constantes

y = 7.74e3  # [N m3]
g = 9.81  # [m/s2]
dh2oi = 62.42796   # [lb / pie3]


def serie_caso_uno(datosfluido, datostuberias, datosacc, efbomba, caudal, dz, dp=0, display=False):
    """
    :param datosfluido: datos fisicos del fluido (densidad, viscosidad cinemática) [kg/m3, m2/s]
    :param datostuberias: dimensiones de tuberias (diametro, longitud, reugosidad) [m, m, m]
    :param datosacc:  datos de elementos (L/D, K) [N.A., N.A.]
    :param efbomba: eficiencia de bomba
    :param caudal: caudal de entrada [m3/s]
    :param dz: diferencial de altura [m]
    :param dp: diferencial de presión [kPa]
    :param display: permite mostrar o no los resultados (bool)
    :return: resultados de análisis de sistema
    """

    # array con resultados
    rdt = np.zeros([len(datostuberias[0]), 5])
    rda = np.zeros([len(datosacc[0])])

    # Calculos por tubería
    for t in range(len(datostuberias[0])):
        rdt[t, 0] = (4*caudal)/(np.pi*np.power(datostuberias[0, t], 2))                               # Velocidad
        rdt[t, 1] = np.power(rdt[t, 0], 2)/(2*g)                                                      # Carga cinética
        rdt[t, 2] = (rdt[t, 0] * datostuberias[0, t] * datosfluido[0])/datosfluido[1]                 # Reynolds
        rdt[t, 3] = util.colebrookfanning(datostuberias[2, t], datostuberias[0, t], rdt[t, 2], 1e-8)  # fanning
        rdt[t, 4] = rdt[t, 3] * (datostuberias[1, t]/datostuberias[0, t]) * rdt[t, 1]                 # Perdidas long.

    # Calculos por nodos (accesorios)
    for n in range(len(datosacc[0])):
        if n < len(datostuberias[0]):
            rda[n] = datosacc[0, n]*datosacc[1, n]*rdt[n, 1]
        else:
            rda[n] = datosacc[0, n] * datosacc[1, n] * rdt[n-1, 1]

    hl = np.sum(rdt[:, 4]) + np.sum(rda)

    ha = (dp/y) + dz + hl

    p = (ha*y*caudal)/efbomba

    res = (rdt, rda, hl, ha, p)

    if display:
        print("Potencia de bomba: ", res[4], "[W]", "=>", res[4] * 0.00134102, " [hp]")

    return res


def serie_caso_dosa(datosfluido, datostuberia, dz=0, dp=0, display=False):
    """
    :param datosfluido: datos fisicos del fluido (densidad, viscosidad cinemática) [kg/m3, m2/s]
    :param datostuberia: dimensiones de tuberias (diametro, longitud, reugosidad) [m, m, m]
    :param dz: diferencial de altura [m]
    :param dp: dp: diferencial de presión [kPa]
    :param display: permite mostrar o no los resultados (bool)
    :return:
    """

    # Calculos por tubería
    hl = (dp/((datosfluido[0]/1000)*g)) + dz
    D = datostuberia[0]
    L = datostuberia[1]
    e = datostuberia[2]

    q = -2.22 * np.power(D, 2)*np.sqrt((g*D*hl)/L) * \
        np.log10((1/(3.7*(D/e))) + (1.784*datosfluido[1]/(D*np.sqrt((g*D*hl)/L))))

    v = (4*q)/(np.pi*np.power(D, 2))

    qmax = (hl, q, v)

    if display:
        print("El caudal máximo es: ", qmax[1], "[m3/s]\n" + "La velocidad máxima: ", qmax[2], "[m/s]")

    return qmax


def serie_caso_dosb(datosfluido, datostuberia, datosacc, cfg, display=False):
    """
    :param datosfluido: datos fisicos del fluido (densidad, viscosidad cinemática) [kg/m3, m2/s]
    :param datostuberia: dimensiones de tuberias (diametro, longitud, reugosidad) [m, m, m]
    :param datosacc: datos de elementos (L/D, K) [N.A., N.A.]
    :param cfg: matriz con configuracion del caso (dz, dp, p1) [m, kPa, kPa]
    :param display: permite mostrar o no los resultados (bool)
    :return:
    """

    def findpresiondos(q):
        v = (4*q)/(np.pi*np.power(datostuberia[0], 2))
        re = (datosfluido[0]*datostuberia[0]*v)/datosfluido[1]
        f = util.colebrookfanning(datostuberia[2], datostuberia[0], re, 5e-8)
        hv = np.power(v,2)/(2*g)
        hl = 0

        for i in range(len(datosacc)):
            hl += datosacc[0, i]*datosacc[1, i]*hv

        hl += f*(datostuberia[1]/datostuberia[0])*hv

        fp = (cfg[2]) + ((datosfluido[0]/1000)*g)*(cfg[0]-hl)-(cfg[2]-cfg[1])

        return fp

    # Calculos por sistema de tuberia
    qi = serie_caso_dosa(datosfluido, datostuberia, cfg[0], cfg[1])[1]

    qop = fsolve(findpresiondos, qi)

    vop = (4 * qop) / (np.pi * np.power(datostuberia[0], 2))
    reop = (datosfluido[0] * datostuberia[0] * vop) / datosfluido[1]
    fop = util.colebrookfanning(datostuberia[2], datostuberia[0], reop, 5e-8)
    hvop = np.power(vop, 2) / (2 * g)
    hlop = 0

    for i in range(len(datosacc)):
        hlop += datosacc[0, i] * datosacc[1, i] * hvop

    hlop += fop * (datostuberia[1] / datostuberia[0]) * hvop

    res = (qop[0], vop[0], reop[0], fop[0], hvop[0], hlop[0])

    if display:
        print("La mejor configuración encontrada es: \nCaudal: %f [m3/s]"
              "\nValocidad: %f [m/s] \nReynolds: %i \nFanning: %f"
              "\nCarga cinética: %f [m] \nPerdidas totales: %f [m]" % res)

    return res


def serie_caso_tresa(datosfluido, datostuberia, q, dz=0, dp=0, display=False):
    """
    :param datosfluido: datos fisicos del fluido. (densidad, viscosidad cinematica) [lb/ft3, ft2/s]
    :param datostuberia: dimensiones de tuberia. (diametro, longitud, rugosidad abs.) [ft, ft]
    :param q: Flujo volumétrico. (Q) [ft3/s]
    :param dz: Carga de altura. [m]
    :param dp: Limite de caida de presión. [psi]
    :return: tuppla con resultados de análisis
    """
    hl = (dp*144/(datosfluido[0])) + dz

    c1 = np.power((datostuberia[0]*np.power(q, 2)/(g*hl)), 4.75)
    c2 = np.power(datostuberia[0]/(g*hl), 5.2)
    d = 0.66*np.power(np.power(datostuberia[1], 1.25)*c1 + datosfluido[1]*np.power(q, 9.4)*c2, 0.04)

    if display:
        print("Diametro mínimo:", d, " [ft]")

    return d


def paralelo_dos_ramas(datosfluido, datostubos, datosacc, dp, display=False):
    """
    :param datosfluido: datos fisicos del fluido. (densidad, viscosidad cinematica) [kg/m3, m2/s]
    :param datosacc: dimesniones de accesorio [longitud equivalente o constante de pérdida]
    :param datostubos: diametros de tuberia evaluada (di, ei) [m, m]
    :param dp: Caida de pesión. [kPa]
    :return: los caudales parciales y el total
    """

    hl = dp/((datosfluido[0]/1000)*g)
    fs = np.zeros([2])

    for itubo in range(len(datostubos[0])):
        fs[itubo] = util.colebrookfanning(datostubos[1, itubo],datostubos[0, itubo], 8e8, 5e-8)

    ksum = np.zeros([2])
    vrama = np.zeros([2])
    qrama = np.zeros([3])

    for irama in range(2):
        for iacc in range(len(datosacc)):
            if datosacc[irama][0, iacc] != 0:
                ksum[irama] += datosacc[irama][0, iacc]
            else:
                ksum[irama] += fs[irama]*datosacc[irama][0, iacc]

        vrama[irama] = np.sqrt(2*g*hl/ksum[irama])
        qrama[irama] = (np.pi*np.power(datostubos[0, irama], 2)/4)*vrama[irama]

    qrama[2] = qrama.sum()

    if display:
        strrst = "Resutados de análisis \n"
        lblrama = "ab"
        for irama in range(2):
            strrst += "\n"
            strrst += "Rama %s \n" % lblrama[irama]
            strrst += "Velocidad: %f [m/s] \n" % vrama[irama]
            strrst += "Caudal: %f [m3/s]  \n" % qrama[irama]
            strrst += "Fanning: %f \n" % fs[irama]
            strrst += "\n"

        strrst += "Totales \n"
        strrst += "Caudal total: %f [m3/s]\n" % qrama[2]
        strrst += "Perdida de carga: %f [m]" % hl
        print(strrst)

    return vrama, qrama, fs
