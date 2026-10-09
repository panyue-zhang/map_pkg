#!/usr/bin/env python3
#coding=utf-8
# ↑ 这两行是 Linux 和 Python 的“身份证”：
# 第1行告诉系统：请用 Python3 来运行我。
# 第2行告诉系统：我的代码里有中文，请用 UTF-8 编码读取，防止乱码。

import rospy
from nav_msgs.msg import OccupancyGrid
# ↑ 引入必要的库：
# rospy 是 ROS 的 Python 核心库。
# nav_msgs.msg 里的 OccupancyGrid 是“占据栅格地图”的消息类型（就是我们要发的包裹类型）。

if __name__ == "__main__" :
    # ↑ 这是 Python 的“主函数”入口。当直接运行这个脚本时，下面的代码才会执行。

    rospy.init_node("map_pub_node")
    # ↑ 初始化 ROS 节点，给这个程序起名叫 "map_pub_node"。

    pub = rospy.Publisher("/map",OccupancyGrid,queue_size=10)
    # ↑ 创建发布者（广播站）：
    # 话题名是 "/map"（地图的标准话题名）。
    # 消息类型是 OccupancyGrid。
    # queue_size=10 表示队列长度，如果消息发太快，最多积压 10 条。

    rate = rospy.Rate(1)
    # ↑ 创建一个频率控制器，设置循环频率为 1 Hz（每秒执行 1 次）。
    # 这意味着地图会每秒刷新一次。

    while not rospy.is_shutdown():
        # ↑ 这是 ROS 节点的“死循环”标准写法。
        # 意思是：“只要 ROS 没被关闭（没按 Ctrl+C），就一直循环”。
        # 对应 C++ 里的 while(ros::ok())。

        msg = OccupancyGrid()
        # ↑ 准备一个“空盒子”，用来装地图数据。

        # --- 填充消息头（Header） ---
        msg.header.frame_id = "map"
        # ↑ 指定地图挂在哪个坐标系下，通常地图都挂在 "map" 坐标系下。
        msg.header.stamp = rospy.Time.now()
        # ↑ 记录当前时间戳（地图生成的时间）。

        # --- 填充地图的元数据（Info） ---
        msg.info.origin.position.x = 0
        msg.info.origin.position.y = 0
        # ↑ 地图原点的位置（0,0）。
        msg.info.resolution = 1.0
        # ↑ 分辨率：真实世界中 1 米，对应地图上的 1 个格子。
        msg.info.width = 4
        msg.info.height = 2
        # ↑ 地图尺寸：宽 4 格，高 2 格（总共 8 个格子）。

        # --- 填充地图的具体数据（Data） ---
        msg.data = [0] * 4 * 2
        # ↑ 【★ Python 特有的神操作 ★】
        # 在 C++ 里我们需要用 resize() 分配内存。
        # 在 Python 里，直接用列表乘法：创建一个包含 8 个 0 的列表。
        # 相当于 msg.data = [0, 0, 0, 0, 0, 0, 0, 0]

        msg.data[0] = 100
        msg.data[1] = 100
        # ↑ 第 1、2 个格子设为 100（代表障碍物，在 RViz 里显示为黑色）。
        msg.data[2] = 0
        # ↑ 第 3 个格子设为 0（代表空地，显示为白色）。
        msg.data[3] = -1
        # ↑ 第 4 个格子设为 -1（代表未知区域，显示为灰色）。

        # 注意：剩下的 msg.data[4] 到 msg.data[7] 默认都是 0（空地）。

        pub.publish(msg)
        # ↑ 把装好的地图盒子发送出去。

        rate.sleep()
        # ↑ 按照 1 Hz 的节奏休息一下，进入下一次循环。