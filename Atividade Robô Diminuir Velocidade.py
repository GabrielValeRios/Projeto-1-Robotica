#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import fabs
from sensor_msgs.msg import LaserScan


velocidade_objetivo = Twist();

# Aqui nós alteramos a velocidade do robô, através da função Twist, daOdometria.
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=3)

def notificacao(data):
 
    global velocidade_objetivo


    #Condição para não dar erros no código.
    if data.ranges[5] < data.range_min:
        return

    elif data.ranges[5] > data.range_max:
        return

    #Aqui definimos o valor da velocidade arbitrariamente,de modo a manter um valor constante, relacionando com a distância, ou seja,
    #se a distância diminuir, a velocidade proporcionalmente também irá diminuir.
    velocidade = data.ranges[5]


    # condição de parada, com uma distância equivalente de 0.45.
    if velocidade < 0.45:
        velocidade = 0

    # Chamada da função Twist()
    velocidade_objetivo = Twist()


    velocidade_objetivo.linear.x = velocidade/5
    velocidade_objetivo.linear.y = 0
    velocidade_objetivo.linear.z = 0




def controle():

    rospy.init_node('Exemplo_Python')

    #Chamada da função notificação, e leitura dos dados do LaserScan.
    rospy.Subscriber("/stable_scan",LaserScan, notificacao)

    #Iniciação do movimento do robô.
    while not rospy.is_shutdown():
        pub.publish(velocidade_objetivo)
        rospy.sleep(0.2)

if __name__ == '__main__':
    try:
        controle()
    except rospy.ROSInterruptException:
        pass

 