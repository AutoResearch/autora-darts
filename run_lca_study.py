from datetime import datetime

import aer_experimentalist.experiment_environment.experiment_config as exp_cfg
from aer.variable import DV_In_Silico as DV
from aer.variable import IVInSilico as IV
from aer.variable import OutputTypes as output_type
from aer_experimentalist.experimentalist_popper import Experimentalist_Popper
from aer_theorist.object_of_study import Object_Of_Study
from aer_theorist.theorist_darts import DARTS_Type, Theorist_DARTS

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
print("date and time =", dt_string)

# GENERAL PARAMETERS

host = exp_cfg.HOST_IP  # ip address of experiment server
port = exp_cfg.HOST_PORT  # port of experiment server

# SIMULATION PARAMETERS

study_name = "LCA"  # name of experiment
max_num_data_points = 500

AER_cycles = 1

# OBJECT OF STUDY

# specify independent variables
x1 = IV(name="x1_lca", value_range=(-1, 1), units="net input", variable_label="x1")

x2 = IV(name="x2_lca", value_range=(-1, 1), units="net input", variable_label="x2")

x3 = IV(name="x3_lca", value_range=(-1, 1), units="net input", variable_label="x3")


# specify dependent variable with type
dx1_lca = DV(
    name="dx1_lca",
    value_range=(0, 1),
    units="net input change",
    variable_label="dx1",
    type=output_type.REAL,
)  # not a probability because sum of activations may exceed 1


# list dependent and independent variables
IVs = [x1, x2, x3]  # only including subset of available variables
DVs = [dx1_lca]

# initialize objects of study
study_object = Object_Of_Study(
    name=study_name, independent_variables=IVs, dependent_variables=DVs
)

# EXPERIMENTALIST

# initialize experimentalist
experimentalist = Experimentalist_Popper(
    study_name=study_name,
    experiment_server_host=host,
    experiment_server_port=port,
)
# THEORIST

# initialize theorist
theorist = Theorist_DARTS(study_name, darts_type=DARTS_Type.ORIGINAL)

# specify plots
theorist.plot(plot=True)

# AUTONOMOUS EMPIRICAL RESEARCH

# seed experiment and split into training/validation set
seed_data = experimentalist.seed(
    study_object, n=max_num_data_points
)  # seed with new experiment
# seed_data = experimentalist.seed(study_object, datafile='experiment_0_data.csv')
# seed with existing data file
study_object.add_data(seed_data)

# add validation set
validation_object_2 = study_object.split(proportion=0.5)
validation_object_2.name = "validation loss"
theorist.add_validation_set(validation_object_2, "validation loss")

# search model ORIGINAL
# model = theorist.search_model(study_object)
#
# # search model FAIR
# theorist_fair = Theorist_DARTS(study_name, darts_type=DARTS_Type.FAIR)
# theorist_fair.plot(plot=True)
# theorist_fair.add_validation_set(validation_object_2, 'validation loss')
# model = theorist_fair.search_model(study_object)
#
# now = datetime.now()
# dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
# print("date and time =", dt_string)
