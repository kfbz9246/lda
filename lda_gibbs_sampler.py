'''
Created on Dec 9, 2018

@author: root
'''
from numpy import zeros, full, multiply, sum, array
from numpy.random import dirichlet, multinomial
from os import getpid, mkdir, rmdir
from os.path import abspath, join
from cPickle import dump

def lda_posterior(data, number_components, alpha=1, beta=1):
    burn_in_samples = 5000
    number_samples = 40005
    number_sets, number_subunits = data.shape
    
    component_distrobution_samples = zeros([number_sets, number_components, number_samples])
    subunit_distrobution_samples = zeros([number_components, number_subunits, number_samples])
    
    component_distrobution_conditional_posterior_parameters = full([number_sets, number_components], alpha)
    subunit_distrobution_conditional_posterior_parameters = full([number_components, number_subunits], beta)
    
    for sets_index in range(number_sets):
        for subunits_index in range(number_subunits):
            components_index = subunits_index% number_components
            subunit_count_in_set = data[sets_index, components_index]
            component_distrobution_conditional_posterior_parameters[sets_index,components_index] += subunit_count_in_set
            subunit_distrobution_conditional_posterior_parameters[components_index, subunits_index] += subunit_count_in_set
            
    
    for sample_number in range(burn_in_samples):
        if sample_number% 100 == 0:
            print 'burnin'
            print sample_number
        component_distrobution_sample = []
        subunit_distrobution_sample = []
        
        for set_component_distrobution_conditional_posterior_parameters in component_distrobution_conditional_posterior_parameters:
            component_distrobution_sample.append(dirichlet(set_component_distrobution_conditional_posterior_parameters))
        component_distrobution_sample = array(component_distrobution_sample)
        
        for component_subunit_distrobution_conditional_posterior_parameters in subunit_distrobution_conditional_posterior_parameters:
            subunit_distrobution_sample.append(dirichlet(component_subunit_distrobution_conditional_posterior_parameters))
        subunit_distrobution_sample = array(subunit_distrobution_sample)
        
        next_component_distrobution_conditional_posterior_parameters = full([number_sets, number_components], alpha)
        next_subunit_distrobution_conditional_posterior_parameters = full([number_components, number_subunits], beta)
        for sets_index in range(number_sets):
            for subunits_index in range(number_subunits):
                component_label_distrobution_conditional_parameters = multiply(component_distrobution_sample[sets_index], subunit_distrobution_sample[:, subunits_index])
                component_label_distrobution_conditional_parameters /= sum(component_label_distrobution_conditional_parameters)
                component_label_counts = multinomial(data[sets_index, subunits_index], component_label_distrobution_conditional_parameters)
                next_component_distrobution_conditional_posterior_parameters[sets_index]+= component_label_counts
                next_subunit_distrobution_conditional_posterior_parameters[:,subunits_index]+=component_label_counts
        component_distrobution_conditional_posterior_parameters = next_component_distrobution_conditional_posterior_parameters
        subunit_distrobution_conditional_posterior_parameters = next_subunit_distrobution_conditional_posterior_parameters
        
    pid_str = str(getpid())
    mkdir(pid_str)
    samples_output_dir_path = abspath(pid_str)

    
    for sample_number in range(number_samples):
        if sample_number% 1000 == 0:
            print sample_number
            samples_output_file_path = join(samples_output_dir_path, str(sample_number))
            samples_output_file = open(samples_output_file_path, 'w')
            dump({'component_distrobution_samples' : component_distrobution_samples, 'subunit_distrobution_samples' : subunit_distrobution_samples}, samples_output_file)
            component_distrobution_samples = zeros([number_sets, number_components, number_samples])
            subunit_distrobution_samples = zeros([number_components, number_subunits, number_samples])
            samples_output_file.close()
            
            
            
        component_distrobution_sample = []
        subunit_distrobution_sample = []
        
        for set_component_distrobution_conditional_posterior_parameters in component_distrobution_conditional_posterior_parameters:
            component_distrobution_sample.append(dirichlet(set_component_distrobution_conditional_posterior_parameters))
        component_distrobution_sample = array(component_distrobution_sample)
        component_distrobution_samples[:,:, sample_number] = component_distrobution_sample
        
        for component_subunit_distrobution_conditional_posterior_parameters in subunit_distrobution_conditional_posterior_parameters:
            subunit_distrobution_sample.append(dirichlet(component_subunit_distrobution_conditional_posterior_parameters))
        subunit_distrobution_sample = array(subunit_distrobution_sample)
        subunit_distrobution_samples[:, :, sample_number] = subunit_distrobution_sample
        
        next_component_distrobution_conditional_posterior_parameters = full([number_sets, number_components], alpha)
        next_subunit_distrobution_conditional_posterior_parameters = full([number_components, number_subunits], beta)
        for sets_index in range(number_sets):
            for subunits_index in range(number_subunits):
                component_label_distrobution_conditional_parameters = multiply(component_distrobution_sample[sets_index], subunit_distrobution_sample[:, subunits_index])
                component_label_distrobution_conditional_parameters /= sum(component_label_distrobution_conditional_parameters)
                component_label_counts = multinomial(data[sets_index, subunits_index], component_label_distrobution_conditional_parameters)
                next_component_distrobution_conditional_posterior_parameters[sets_index]+= component_label_counts
                next_subunit_distrobution_conditional_posterior_parameters[:,subunits_index]+=component_label_counts
        component_distrobution_conditional_posterior_parameters = next_component_distrobution_conditional_posterior_parameters
        subunit_distrobution_conditional_posterior_parameters = next_subunit_distrobution_conditional_posterior_parameters
    return component_distrobution_samples, subunit_distrobution_samples
                
    
            

































        