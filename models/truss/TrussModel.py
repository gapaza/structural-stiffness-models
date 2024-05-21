import config
import time


from models.truss.TrussVolumeFraction import TrussVolumeFraction
from models.truss.TrussStiffness import TrussStiffness



class TrussModel:

    def __init__(self, sidenum):
        self.sidenum = sidenum

    def evaluate(self, design_array, y_modulus, member_radii, member_length):

        # 1. Calculate the volume fraction
        curr_time = time.time()
        vf_client = TrussVolumeFraction(self.sidenum, design_array)
        design_conn_array = vf_client.design_conn_array
        # volume_fraction, feasibility_constraint, interaction_list = vf_client.evaluate(member_radii, member_length)
        volume_fraction, feasibility_constraint, interaction_list = 0, 0, 0

        print("Time taken for volume fraction: ", time.time() - curr_time)

        # 2. Calculate the stiffness
        curr_time = time.time()
        v_stiff, h_stiff, stiff_ratio = TrussStiffness.evaluate(design_conn_array, self.sidenum, member_length, member_radii, y_modulus)
        print("Time taken for stiffness: ", time.time() - curr_time)

        # print("Volume fraction: ", volume_fraction)
        # print("Vertical stiffness: ", v_stiff)
        # print("Horizontal stiffness: ", h_stiff)
        # print("Stiffness ratio: ", stiff_ratio)
        # print("Feasibility constraint: ", feasibility_constraint)

        return v_stiff, h_stiff, stiff_ratio, volume_fraction, feasibility_constraint




if __name__ == '__main__':

    sidenum = config.sidenum
    design_array = [1 for x in range(config.num_vars)]
    y_modulus = 1816200.0
    member_radii = 250e-6
    member_length = 0.01

    truss_model = TrussModel(sidenum)
    curr_time = time.time()
    truss_model.evaluate(design_array, y_modulus, member_radii, member_length)
    print("Time taken: ", time.time() - curr_time)
