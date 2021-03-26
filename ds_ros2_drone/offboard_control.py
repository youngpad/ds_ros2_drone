import rclpy
from rclpy.node import Node

# Import msgs
from ds_ros2_msgs.msg import OffboardControlMode
from ds_ros2_msgs.msg import TrajectorySetpoint
from ds_ros2_msgs.msg import VehicleCommand
from ds_ros2_msgs.msg import VehicleControlMode # hva brukes denne til?


# Create drone offboard control class
class DroneOffboardControl(Node):

    def __init__(self):
        # Init
        super().__init__('drone_offboard_control')

        # Create subscriber
        self.subscription = self.create_subscription(TrajectorySetpoint, 'use_drone_setpoint', self.update_trajectory_setpoint, 10)

        # Create publishers
        self.offboard_control_mode_publisher_ = self.create_publisher(OffboardControlMode, 'OffboardControlMode_PubSubTopic', 10)
        self.trajectory_setpoint_publisher_ = self.create_publisher(TrajectorySetpoint, 'TrajectorySetpoint_PubSubTopic', 10)
        self.vehicle_command_publisher_ = self.create_publisher(VehicleCommand, 'VehicleCommand_PubSubTopic', 10)

        # Member variables
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.yaw = 0.0

        # Create timer
        timer_period = 0.1 # 100ms
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # Shit happens here
        self.arm() # Run this once at startup to arm the drone
        self.publish_offboard_control_mode() # Run this once at startup to tell drone that it will recieve only positional data
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_DO_SET_MODE, 1, 6)

    # This function re
    def timer_callback(self):
        self.publish_offboard_control_mode()
        self.publish_trajectory_setpoint()

    # Callback method that updates the current trajectory setpoint
    def update_trajectory_setpoint(self, msg):
        # Update member variables with respect to incoming trajectory setpoint
        msg.x = self.x
        msg.y = self.y
        msg.z = self.z
        msg.yaw = self.yaw

    # This method arms the drone when called
    def arm(self):
        # Call member method that publishes vehicle commands
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 1.0, 0.0)
        self.get_logger().info('Arm command sent')

    # This method disarms the drone when called
    def disarm(self):
        # Call member method that publishes vehicle commands
        self.publish_vehicle_command(VehicleCommand.VEHICLE_CMD_COMPONENT_ARM_DISARM, 0.0, 0.0)
        self.get_logger().info('Disarm command sent')

    # Method that publishes offboard control mode
    def publish_offboard_control_mode(self):
        # Define OffboardControlMode message type
        msg = OffboardControlMode()

        # msg.timestamp , trenger man denne?
        msg.position = True
        msg.velocity = False
        msg.acceleration = False
        msg.attitude = False
        msg.body_rate = False

        # Publish offboard control mode message
        self.offboard_control_mode_publisher_.publish(msg)

    # Method that publishes trajectory setpoint
    def publish_trajectory_setpoint(self):
        # Define TrajectorySetpoint message type
        msg = TrajectorySetpoint()

        #msg.timestamp , trenger man denne?
        msg.x = self.x
        msg.y = self.y
        msg.z = self.z
        msg.yaw = self.yaw

        # Publish trajectory setpoint
        self.trajectory_setpoint_publisher_.publish(msg)

    # Method that publishes vehicle commands
    def publish_vehicle_command(self, command, param1, param2):
        # Define VehicleCommand message type
        msg = VehicleCommand()

        # msg.timestamp , trenger man denne?
        msg.param1 = float(param1)
        msg.param2 = float(param2)
        msg.command = command
        msg.target_system = 1
        msg.target_component = 1
        msg.source_system = 1
        msg.source_component = 1
        msg.from_external = True

        # Publish vehicle command message
        self.vehicle_command_publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)

    drone_offboard_control = DroneOffboardControl()

    rclpy.spin(drone_offboard_control)

    drone_offboard_control.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
