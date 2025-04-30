from launch_ros.actions import Node
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
import xacro
import os
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    share_dir = get_package_share_directory('left_robot_description')

    xacro_file = os.path.join(share_dir, 'urdf', 'left_robot.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    robot_urdf = robot_description_config.toxml()

    right_share_dir = get_package_share_directory('right_robot_description')

    right_xacro_file = os.path.join(right_share_dir, 'urdf', 'right_robot.xacro')
    right_robot_description_config = xacro.process_file(right_xacro_file)
    right_robot_urdf = right_robot_description_config.toxml()

    rviz_config_file = os.path.join(share_dir, 'config', 'dual_display.rviz')

    left_zeros = {"zeros": {
        "LJ1": 3.14159265359,
        "LJ2": 0.0,
        "LJ3": 1.57079632679,
        "LJ4": 0.0,
        "LJ5": 1.57079632679,
        "LJ6": 1.57079632679,
        "LJ7": 0.0,
    }}

    right_zeros = {"zeros": {
        "RJ1": 0.0,
        "RJ2": 3.14159265359,
        "RJ3": 1.57079632679,
        "RJ4": 0.0,
        "RJ5": 1.57079632679,
        "RJ6": 1.57079632679,
        "RJ7": 0.0,
    }}

    gui_arg = DeclareLaunchArgument(
        name='gui',
        default_value='True'
    )

    show_gui = LaunchConfiguration('gui')

    left_robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='left_robot_state_publisher',
        namespace='left',
        parameters=[
            {'robot_description': robot_urdf}
        ]
    )

    right_robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='right_robot_state_publisher',
        namespace='right',
        parameters=[
            {'robot_description': right_robot_urdf}
        ]
    )

    left_joint_state_publisher_node = Node(
        condition=UnlessCondition(show_gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[left_zeros],
        name='left_joint_state_publisher',
        namespace='left'
    )

    left_joint_state_publisher_gui_node = Node(
        condition=IfCondition(show_gui),
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        parameters=[left_zeros],
        name='left_joint_state_publisher_gui',
        namespace='left',
    )

    right_joint_state_publisher_node = Node(
        condition=UnlessCondition(show_gui),
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[right_zeros],
        name='right_joint_state_publisher',
        namespace='right'
    )

    right_joint_state_publisher_gui_node = Node(
        condition=IfCondition(show_gui),
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        parameters=[right_zeros],
        name='right_joint_state_publisher_gui',
        namespace='right',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_file],
        output='screen'
    )

    return LaunchDescription([
        gui_arg,
        left_robot_state_publisher_node,
        right_robot_state_publisher_node,
        left_joint_state_publisher_node,
        left_joint_state_publisher_gui_node,
        right_joint_state_publisher_node,
        right_joint_state_publisher_gui_node,
        rviz_node
    ])
