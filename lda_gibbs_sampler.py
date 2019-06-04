'''
Created on Dec 9, 2018

@author: root
'''
from numpy import zeros, full, multiply, sum, array, empty, arange
from numpy.random import dirichlet, multinomial
from os import getpid, mkdir, rmdir
from os.path import abspath, join
from cPickle import dump

def lda_posterior(data, number_components, sample_dir_path, number_samples, thinning_factor=10, sample_output_size=100, alpha=1, beta=1,):
    number_sets, number_subunits = data.shape
    
    component_distrobution_conditional_posterior_parameters = full([number_sets, number_components], alpha)
    subunit_distrobution_conditional_posterior_parameters = full([number_components, number_subunits], beta)
    
    for sets_index in range(number_sets):
        for subunits_index in range(number_subunits):
            components_index = subunits_index% number_components
            subunit_count_in_set = data[sets_index, components_index]
            component_distrobution_conditional_posterior_parameters[sets_index,components_index] += subunit_count_in_set
            subunit_distrobution_conditional_posterior_parameters[components_index, subunits_index] += subunit_count_in_set
            
    next_sample_subset_size = sample_output_size if sample_output_size < number_samples else number_samples
    component_distrobution_samples = empty((number_sets, number_components, next_sample_subset_size))
    subunit_distrobution_samples = empty((number_components, number_subunits, next_sample_subset_size))
    
    samples_in_subset_counter = 0
    kelson = thinning_factor -1
    for sample_number in range(number_samples):
        for thinning_counter in range(thinning_factor):
            component_distrobution_sample = empty((number_sets, number_components))
            for set_index, set_component_distrobution_conditional_posterior_parameters in enumerate(component_distrobution_conditional_posterior_parameters):
                component_distrobution_sample[set_index] = dirichlet(set_component_distrobution_conditional_posterior_parameters)
            
            
            subunit_distrobution_sample = empty((number_components, number_subunits))
            for component_index, component_subunit_distrobution_conditional_posterior_parameters in enumerate(subunit_distrobution_conditional_posterior_parameters):
                subunit_distrobution_sample[component_index] = dirichlet(component_subunit_distrobution_conditional_posterior_parameters)
            
            if thinning_counter == kelson:
                component_distrobution_samples[:,:,int(samples_in_subset_counter)] = component_distrobution_sample
                subunit_distrobution_samples[:,:,int(samples_in_subset_counter)] = subunit_distrobution_sample
            
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
        samples_in_subset_counter += 1

        if samples_in_subset_counter >= next_sample_subset_size:
            samples_output_file_path = join(sample_dir_path, str(sample_number+1))
            samples_output_file = open(samples_output_file_path, 'w')
            component_distrobution_samples = array(component_distrobution_samples)
            subunit_distrobution_samples = array(subunit_distrobution_samples)
            dump({'component_distrobution_samples' : component_distrobution_samples, 'subunit_distrobution_samples' : subunit_distrobution_samples}, samples_output_file)
            samples_output_file.close()
            number_samples_left = number_samples - sample_number - 1
            next_sample_subset_size = sample_output_size if sample_output_size < number_samples_left else number_samples_left
            component_distrobution_samples = empty((number_sets, number_components, next_sample_subset_size))
            subunit_distrobution_samples = empty((number_components, number_subunits, next_sample_subset_size))
            samples_in_subset_counter = 0
            

































        