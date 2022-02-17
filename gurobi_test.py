import gurobipy as gp
import numpy as np


def main():
    m = gp.Model()

    X0 =np.array([0, 0]).reshape([2, 1])
    print(X0)



if __name__ == "__main__":
    main()