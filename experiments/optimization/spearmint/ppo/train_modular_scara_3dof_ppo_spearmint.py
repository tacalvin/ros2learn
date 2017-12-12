import gym
import gym_gazebo
import tensorflow as tf
import argparse
import copy
import sys
import numpy as np

from baselines import logger
from baselines.common import set_global_seeds, tf_util as U
from baselines.ppo1 import mlp_policy, pposgd_simple

# from baselines.agent.utility.general_utils import get_ee_points, get_position


#def train_setup(job_id, max_t, t_per_actorbatch, optim_ep, optim_batchs, l):
def train_setup(job_id, t_per_actorbatch, optim_ep, optim_batchs):
    env = gym.make('GazeboModularScara3DOF-v3')
    initial_observation = env.reset()
    print("Initial observation: ", initial_observation)
    env.render()
    seed = 0
    model_name = 'ros1_ppo1_test_O'+str(job_id)+'_'

    U.make_session(num_cpu=1).__enter__()
    set_global_seeds(seed)

    env.seed(seed)
    def policy_fn(name, ob_space, ac_space):
        return mlp_policy.MlpPolicy(name=name, ob_space=ob_space, ac_space=ac_space,
            hid_size=64, num_hid_layers=2)


    t_per_actorbatch_i = list(map(int, t_per_actorbatch))
    optim_batchsize_i = list(map(int, optim_batchs))
    #print("timesteps_per_actorbatch", t_per_actorbatch)
    #print("optim_epochs", optim_ep)
    #print("optim_batch", optim_batchs)

    #print("t_per_actorbatch_i", t_per_actorbatch_i)
    #print("optim_batchsize_i", optim_batchsize_i)
    #print("max_timesteps", int(max_t))
    print("timesteps_per_actorbatch", t_per_actorbatch_i[0])
    print("optim_epochs", int(optim_ep))
    print("optim_batchsize", optim_batchsize_i[0])
    #print("timesteps_per_actorbatch[1]", t_per_actorbatch_i[1])
    #print("optim_batchsize[1]", optim_batchsize_i[1])

    #print("lam", float(l))
    optim_metric = pposgd_simple.learn(env, policy_fn,
                        max_timesteps=1e6,
                        timesteps_per_actorbatch=t_per_actorbatch_i[0],
                        clip_param=0.2, entcoeff=0.0,
                        optim_epochs=int(optim_ep), optim_stepsize=3e-04, gamma=0.99,
                        #optim_batchsize=optim_batchsize_i[0], lam=float(l), schedule='linear', save_model_with_prefix=model_name)
                        optim_batchsize=optim_batchsize_i[0], lam=0.95, schedule='linear', save_model_with_prefix=model_name)


    return optim_metric

def main(job_id, params):
    return train_setup(job_id, params['timesteps_per_actorbatch'], params['optim_epochs'], params['optim_batchsize'])