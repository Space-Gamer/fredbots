#!/usr/bin/env python3
#the same q learning model with atom now 
import gym
from gym import spaces
import rospy
from std_srvs.srv import Empty
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from math import pow, atan2, sqrt
import numpy as np
from gazebo_msgs.srv import SetModelState
from gazebo_msgs.msg import ModelState



class AtomEnv(gym.Env):
    def __init__(self):
        super(AtomEnv, self).__init__()
        rospy.init_node('atom_move', anonymous=True)
        self.velocity_publisher = rospy.Publisher('/atom/cmd_vel', Twist, queue_size=10)
        self.pose_subscriber = rospy.Subscriber('/atom/odom', Odometry, self.update_pose)
        # self.reset_proxy = rospy.ServiceProxy('/reset', Empty)

        self.set_model_state_proxy = rospy.ServiceProxy('/gazebo/set_model_state', SetModelState)

        self.model_state_msg = ModelState()
        self.model_state_msg.model_name = 'atom'
        self.model_state_msg.pose.position.x = 0.0
        self.model_state_msg.pose.position.y = 0.0
        self.model_state_msg.pose.position.z = 0.0
        self.model_state_msg.pose.orientation.x = 0.0
        self.model_state_msg.pose.orientation.y = 0.0
        self.model_state_msg.pose.orientation.z = 0.0
        self.model_state_msg.pose.orientation.w = 1.0

        self.action_space = spaces.Discrete(4)  # Up, Down, Left, Right
        self.observation_space = spaces.Box(low=0, high=10, shape=(4,))
        self.rate = rospy.Rate(10)
        self.goal_x = 3   # destination coordinates
        self.goal_y = 3
        # self.position_x = 0  # init coordinates
        # self.position_y = 0
        self.position_x = 0  # init coordinates
        self.position_y = 0
        self.episodes = 5
        self.learning_rate = 0.5
        self.discount_factor = 0.99
        self.epsilon = 0.2
        self.q_table = np.zeros((10, 10, 4))
    
    def update_pose(self, data):
        self.position_x = round(data.pose.pose.position.x, 2)
        self.position_y = round(data.pose.pose.position.y, 2)

    def reset(self):
        
        # self.reset_proxy()  # Reset the turtlesim simulation
        self.position_x = 0
        self.position_y = 0    # reset to init coordinates
        return self.get_observation()
    
    def step(self, action):
        self.move_atom(action)
        self.rate.sleep()
        obs = self.get_observation()
        reward = self.get_reward()
        done = self.is_done()
        return obs, reward, done, {}

    def move_atom(self, action):
        if action == 0:  # Up
            self.move(5.0, 0.0)
            self.move(40.0, 0.0)
        elif action == 1:  # Down
            self.move(-5.0, 0.0)
            self.move(-40.0, 0.0)
        elif action == 2:  # Left
            self.move(0.0, 5.0)
            self.move(0.0, 40.0)
        elif action == 3:  # Right
            self.move(0.0, -5.0)
            self.move(0.0, -40.0)

    def move(self, linear_vel, angular_vel):
        velocity_msg = Twist()
        velocity_msg.linear.x = linear_vel
        velocity_msg.angular.z = angular_vel
        self.velocity_publisher.publish(velocity_msg)

    def get_observation(self):
        return [self.goal_x, self.goal_y, self.position_x, self.position_y]
    
    def get_reward(self):
        distance_to_goal = sqrt(pow(self.goal_x - self.position_x, 2) + pow(self.goal_y - self.position_y, 2))
        reward = -distance_to_goal
        return reward
    
    def is_done(self):
        dist_bound = sqrt(pow(0 - self.position_x, 2) + pow(0 - self.position_y, 2))
        print("dist_bound ",dist_bound)
        if dist_bound > 2:
            response = self.set_model_state_proxy(self.model_state_msg)
            print("reset DONE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        distance_threshold = 0.5
        distance_to_goal = sqrt(pow(self.goal_x - self.position_x, 2) + pow(self.goal_y - self.position_y, 2))
        return distance_to_goal < distance_threshold
    
    def q_learning(self):
        for episode in range(self.episodes):
            state = self.reset()
            done = False
            while not done:
                print("\n\nEpisode no. : ",episode+1)
                print("Overall State : ",state)
                state_index = self.get_state_index(state)
                print("Current State ",state[2],state[3])
                print("Goal State ",state[0],state[1])
                action = self.get_action(state_index)
                print("Action ",action)
                next_state, reward, done, _ = self.step(action)
                print("next state ",next_state[2],next_state[3])
                next_state_index = self.get_state_index(next_state)
                # print("Next State ",next_state_index)
                print("Reward ", reward)
                current_q_value = self.q_table[state_index][action]
                print("Old_Q_Value ",current_q_value)
                max_q_value = np.max(self.q_table[next_state_index])
                print("Max Q Value of Present State ", max_q_value)
                new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (reward + self.discount_factor * max_q_value)
                print("New_Q_Value of Present State ",new_q_value)
                self.q_table[state_index][action] = new_q_value
                state = next_state
            print(f"Episode: {episode + 1} completed.")

    def get_state_index(self, state):        # return np.argmax(self.q_table[x][y])
        x = int(state[2])  # position_x
        y = int(state[3])  # position_y
        return x, y
    
    def get_action(self, state_index):
        x, y = state_index
        # return np.argmax(self.q_table[x][y])
        if np.random.random() < self.epsilon:
            return np.argmax(self.q_table[x,y])
        else:
            return np.random.randint(4)        
if __name__ == '__main__':
    env = AtomEnv()
    env.q_learning()