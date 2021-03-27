from setuptools import setup

package_name = 'ds_ros2_drone'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='martinmaeland',
    maintainer_email='martinmaeland@outlook.com',
    description='ROS2 package for offboard control of Pixhawk 4 mini.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'offboard_control = ds_ros2_drone.offboard_control:main'
        ],
    },
)
