import gym
from gym import spaces
import gym_gazebo

import numpy as np
import pandas
from baselines import deepq
from  baselines.deepq import models
from  baselines.deepq import build_graph_robotics
from  baselines.deepq import replay_buffer
from  baselines.deepq.simple_robotics import learn, load
import tensorflow as tf


env = gym.make("GazeboModularScara3DOF-v2")

logdir = '/tmp/rosrl/' + str(env.__class__.__name__) +'/deepq/monitor/'
logger.configure(os.path.abspath(logdir))
print("logger.get_dir(): ", logger.get_dir() and os.path.join(logger.get_dir()))
env = bench.MonitorRobotics(env, logger.get_dir() and os.path.join(logger.get_dir()), allow_early_resets=True) #, allow_early_resets=True
gym.logger.setLevel(logging.WARN)

#Discrete actions
goal_average_steps = 2
max_number_of_steps = 20
last_time_steps = np.ndarray(0)
n_bins = 10
epsilon_decay_rate = 0.99 ########
it = 1 ######

# tf.reset_default_graph()

# Number of states is huge so in order to simplify the situation
# typically, we discretize the space to: n_bins ** number_of_features
joint1_bins = pandas.cut([-np.pi/2, np.pi/2], bins=n_bins, retbins=True)[1][1:-1]
joint2_bins = pandas.cut([-np.pi/2, np.pi/2], bins=n_bins, retbins=True)[1][1:-1]
joint3_bins = pandas.cut([-np.pi/2, np.pi/2], bins=n_bins, retbins=True)[1][1:-1]
action_bins = pandas.cut([-np.pi/2, np.pi/2], bins=n_bins, retbins=True)[1][1:-1]

difference_bins = abs(joint1_bins[0] - joint1_bins[1])
action_bins = [(difference_bins, 0.0, 0.0), (-difference_bins, 0.0, 0.0),
        (0.0, difference_bins, 0.0), (0.0, -difference_bins, 0.0),
        (0.0, 0.0, difference_bins), (0.0, 0.0, -difference_bins),
        (0.0, 0.0, 0.0)]
discrete_action_space = spaces.Discrete(7)
with tf.variable_scope("dpq" + str(job_id)):
    # graph = tf.Graph()
    with tf.Session(config=tf.ConfigProto()) as session:
        model = models.mlp([64])

        print("learning rate", learning_rate)
        print("gam", gam)
        print("max_timesteps", max_t)
        print("buffer size", buff_size)
        print("learning starts", lr_start)


        act, mean_rew = learn(
            env,
            q_func=model,
            lr=float(learning_rate),
            gamma=float(gam),
            max_timesteps=int(max_t),
            buffer_size=int(buff_size),
            checkpoint_freq = 100,
            learning_starts = int(lr_start),
            target_network_update_freq = 100,
            exploration_fraction=0.1,
            exploration_final_eps=0.02,
            print_freq=10,
            callback=callback, job_id=str(job_id))

        print("MEAN REWARD", mean_rew, "Job id: ", job_id, "Actor: ", act)
        act.save("scara_model_" + str(job_id) + ".pkl")