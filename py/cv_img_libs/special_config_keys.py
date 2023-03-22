 


def create_special_keys(dt):
    try:

        if("compare_args" not in dt):
            print("Not there")

        if("hang_isue_checker" not in dt):
            print("not there1")
        
        try:
            if( dt["compare_args"]["similarity"]["m1_powered_on"] == None):
                print("not there2")
        except:
                print("not there2 - except")

        if("BRISK_FLANN_gp_gpp_check_enabled" not in dt["compare_args"]["BRISK_FLANN_parametric"]):
            print("not there3")


        
    except:
        pass
    
    return dt

    