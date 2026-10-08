// 1. 引入必要的头文件
#include <ros/ros.h>
#include <nav_msgs/OccupancyGrid.h> // ★ 引入“占据栅格地图”消息类型

int main(int argc, char *argv[])
{
    // 2. 初始化 ROS 节点
    ros::init(argc, argv, "map_pub_node"); // 节点名为 "map_pub_node"
    ros::NodeHandle n; // 创建节点句柄（大管家）

    // 3. 创建发布者
    // 发布到 "/map" 话题，消息类型是 nav_msgs::OccupancyGrid，队列长度 10
    ros::Publisher pub = n.advertise<nav_msgs::OccupancyGrid>("/map", 10);

    // 4. 设置循环频率
    ros::Rate r(1); // 每秒执行 1 次（1 Hz），意味着地图每秒刷新一次

    // 5. 进入主循环
    while(ros::ok())
    {
        // 6. 准备地图消息包
        nav_msgs::OccupancyGrid msg;

        // --- 7. 填充“消息头（Header）” ---
        // 指定地图的坐标系，通常地图都挂在 "map" 坐标系下
        msg.header.frame_id = "map";
        // 记录当前时间戳（也就是地图生成的时间）
        msg.header.stamp = ros::Time::now();

        // --- 8. 填充“地图元数据（Info）” ---
        // 地图原点位置（相对 map 坐标系）
        msg.info.origin.position.x = 0;
        msg.info.origin.position.y = 0;
        
        // 地图分辨率：1.0 米/像素（真实世界中 1 米对应地图上的 1 个格子）
        msg.info.resolution = 1.0; 
        
        // 地图尺寸：宽 4 格，高 2 格（也就是一个 4x2 的网格）
        msg.info.width = 4;
        msg.info.height = 2;

        // --- 9. 填充“地图数据（Data）” ---
        // 地图总格子数 = 宽 * 高 = 4 * 2 = 8 个格子
        // resize 函数分配内存空间，准备存放 8 个数据
        msg.data.resize(4*2); 

        // 给这 8 个格子赋值（数字含义通常是：0=空地，100=障碍物，-1=未知区域）
        msg.data[0] = 100; // 第1格：障碍物（黑）
        msg.data[1] = 100; // 第2格：障碍物（黑）
        msg.data[2] = 0;   // 第3格：空地（白）
        msg.data[3] = -1;  // 第4格：未知区域（灰）
        // 注意：msg.data[4] 到 msg.data[7] 默认值为 0（空地）

        // 10. 发布地图消息
        pub.publish(msg);

        // 11. 休眠，等待下一个循环
        r.sleep();
    }
    
    return 0;
}