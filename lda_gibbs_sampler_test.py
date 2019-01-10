'''
Created on Dec 10, 2018

@author: root
'''

from numpy import matmul, array, zeros
from random import sample
from lda_gibbs_sampler import lda_posterior
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import figure
from cPickle import load()

subunits_distrobutions = [[.6,.4,0,0,0,0,0,0,0,0],
                          [0,.1,.6,.3,0,0,0,0,0,0],
                          [0,0,0,.1,.6,.3,0,0,0,0],
                          [0,0,0,0,0,.1,.6,.3,0,0],
                          [0,0,0,0,0,0,0,.1,.6,.3]]
                        #[0,0,0,0,.2,.1,.4,.3,0],
                        #[0,0,0,0,0,0,.2,.1,.4,.3]]

number_components = len(subunits_distrobutions)
'''components_distrobutions = [[.5,.5,0,0,0,0,0],
                            [0,.5,.5,0,0,0,0],
                            [0,0,.5,.5,0,0,0],
                            [0,0,0,.5,.5,0,0],
                            [0,0,0,0,.5,.5,0],
                            [0,0,0,0,0,.5,.5],
                            [.5,.5,0,0,0,0,0],
                            [0,.5,.5,0,0,0,0],
                            [0,0,.5,.5,0,0,0],
                            [0,0,0,.5,.5,0,0],
                            [0,0,0,0,.5,.5,0],
                            [0,0,0,0,0,.5,.5]]
'''
components_distrobutions = []
next_component_distrobution_non_zero_indeces_posibilites = range(number_components)
for index in range(100):
    next_component_distrobution = [0]*number_components
    next_component_distrobution_non_zero_indeces = sample(next_component_distrobution_non_zero_indeces_posibilites, 2)
    print next_component_distrobution_non_zero_indeces
    for next_component_distrobution_non_zero_index in next_component_distrobution_non_zero_indeces:
        next_component_distrobution[next_component_distrobution_non_zero_index] = .5
    components_distrobutions.append(next_component_distrobution)
    
data = matmul(array(components_distrobutions), array(subunits_distrobutions))
data *= 100000


lda_posterior(data,number_components, 'test_output', 1000, 1001)
'''
for components_index in range(7):
    fig = figure(figsize=(11, 11), dpi=96, frameon=True)
    fig_ax = fig.add_subplot(111)
    fig_ax.hist(component_distrobution_samples[0, components_index], 100)
    fig.savefig(str(components_index)+'.png', bbox_inches='tight')
'''
exit()
subunit_distrobution_samples = []
for subunits_index in range(10):
    fig = figure(figsize=(11, 11), dpi=96, frameon=True)
    fig_ax = fig.add_subplot(111)
    fig_ax.hist(subunit_distrobution_samples[1, subunits_index], 100)
    fig.savefig(str(subunits_index)+'.png', bbox_inches='tight')
    
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    