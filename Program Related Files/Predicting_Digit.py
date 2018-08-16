import predict_2 as digit_predictor
import os,sys

#path = 'Digits_Prepared/'

def get_digits_in_list(path_to_prepared_images, grouped_digit_filename):
    digits = []
    for a in grouped_digit_filename:
        elem = []
        for filename in a:
            x = digit_predictor.predict(path_to_prepared_images+filename)
            elem.append(x)
        digits.append(elem)
        #os.remove(path+filename)
    return digits

def main():
    digits=get_digits_in_list()
    print (digits)
if __name__ == "__main__":
    main()
