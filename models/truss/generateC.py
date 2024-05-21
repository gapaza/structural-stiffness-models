import numpy as np

from models.truss.formK import formK

def generateC(sel, rvar, NC, CA, Avar, E, C, sidenum):
    uBasket = []
    FBasket = []

    # Iterate through each strain component
    for y in range(3):

        # Define vectors to hold indexes for output forces
        Fi_x = []
        Fi_y = []
        Fi_xy = []

        strainvec = np.zeros(3)
        strainvec[y] = 0.01
        strainvec[2] *= 2

        e11, e22, e12 = strainvec

        if e11 != 0 or e22 != 0:
            K = formK(NC, CA, Avar, E)
            u_r = []
            F_q = []
            qvec = []
            rvec = []

            for x in range(len(NC)):
                ND = NC / sel
                if ND[x, 0] in [0, 1] or ND[x, 1] in [0, 1]:
                    if ND[x, 0] == 0:
                        u_r.append(0)
                        rvec.append(2 * x)
                    elif ND[x, 0] == 1:
                        u_r.append(e11 * sel)
                        rvec.append(2 * x)
                        Fi_x.append(2 * x)
                    elif ND[x, 1] == 0 and e22 != 0:
                        u_r.append(0)
                        rvec.append(2 * x)
                    else:
                        F_q.append(0)
                        qvec.append(2 * x)

                    if ND[x, 1] == 0:
                        u_r.append(0)
                        rvec.append(2 * x + 1)
                    elif ND[x, 1] == 1:
                        u_r.append(e22 * sel)
                        rvec.append(2 * x + 1)
                        Fi_y.append(2 * x + 1)
                        Fi_xy.append(2 * x)
                    elif ND[x, 0] == 0 and e11 != 0:
                        u_r.append(0)
                        rvec.append(2 * x)
                    else:
                        F_q.append(0)
                        qvec.append(2 * x + 1)
                else:
                    F_q.append(0)
                    F_q.append(0)
                    qvec.append(2 * x)
                    qvec.append(2 * x + 1)

            qrvec = qvec + rvec
            newK = K[np.ix_(qrvec, qrvec)]
            K_qq = newK[:len(qvec), :len(qvec)]
            K_rq = newK[len(qvec):, :len(qvec)]
            K_qr = newK[:len(qvec), len(qvec):]
            K_rr = newK[len(qvec):, len(qvec):]
            u_q = np.linalg.solve(K_qq, np.array(F_q) - K_qr @ np.array(u_r))
            F_r = K_rq @ u_q + K_rr @ np.array(u_r)
            altu = np.concatenate((u_q, u_r))
            altF = np.concatenate((F_q, F_r))
            F = np.zeros(len(altF))
            u = np.zeros(len(altu))
            for i, val in enumerate(qrvec):
                F[val] = altF[i]
                u[val] = altu[i]
        else:
            K = formK(NC, CA, Avar, E)
            u_r = []
            F_q = []
            qvec = []
            rvec = []

            for x in range(len(NC)):
                ND = NC / sel
                if ND[x, 0] in [0, 1] or ND[x, 1] in [0, 1]:
                    if ND[x, 0] == 0:
                        u_r.append(e12 * sel * ND[x, 1])
                        rvec.append(2 * x)
                    elif ND[x, 0] == 1:
                        u_r.append(e12 * sel * ND[x, 1])
                        rvec.append(2 * x)
                        Fi_x.append(2 * x)
                    elif ND[x, 1] == 1:
                        u_r.append(e12 * sel)
                        rvec.append(2 * x)
                    elif ND[x, 1] == 0:
                        u_r.append(0)
                        rvec.append(2 * x)
                    else:
                        F_q.append(0)
                        qvec.append(2 * x)

                    if ND[x, 1] == 0:
                        u_r.append(0)
                        rvec.append(2 * x + 1)
                    elif ND[x, 1] == 1:
                        u_r.append(0)
                        rvec.append(2 * x + 1)
                        Fi_y.append(2 * x + 1)
                        Fi_xy.append(2 * x)
                    else:
                        F_q.append(0)
                        qvec.append(2 * x + 1)
                else:
                    F_q.append(0)
                    F_q.append(0)
                    qvec.append(2 * x)
                    qvec.append(2 * x + 1)

            qrvec = qvec + rvec
            newK = K[np.ix_(qrvec, qrvec)]
            K_qq = newK[:len(qvec), :len(qvec)]
            K_rq = newK[len(qvec):, :len(qvec)]
            K_qr = newK[:len(qvec), len(qvec):]
            K_rr = newK[len(qvec):, len(qvec):]
            u_q = np.linalg.solve(K_qq, np.array(F_q) - K_qr @ np.array(u_r))
            F_r = K_rq @ u_q + K_rr @ np.array(u_r)
            altu = np.concatenate((u_q, u_r))
            altF = np.concatenate((F_q, F_r))
            F = np.zeros(len(altF))
            u = np.zeros(len(altu))
            for i, val in enumerate(qrvec):
                F[val] = altF[i]
                u[val] = altu[i]

        horizrads = [rvar[i] for i in range(len(CA)) if
                     (CA[i, 0] + sidenum == CA[i, 1]) and (NC[CA[i, 0] - 1, 1] == sel)]
        vertrads = [rvar[i] for i in range(len(CA)) if (CA[i, 0] + 1 == CA[i, 1]) and (NC[CA[i, 0] - 1, 0] == sel)]
        horizmean = np.mean(horizrads)
        vertmean = np.mean(vertrads)

        F_x = sum(F[Fi_x])
        F_y = sum(F[Fi_y])
        F_xy = sum(F[Fi_xy])
        stressvec = np.array([F_x / (sel * 2 * vertmean), F_y / (sel * 2 * horizmean), F_xy / (sel * 2 * horizmean)])

        if y == 0:
            stresses = stressvec

        C[:, y] = stressvec / strainvec[y]
        FBasket.append(F)
        uBasket.append(u)

    return C, np.array(uBasket), np.array(FBasket)



if __name__ == '__main__':

    # Mock inputs for testing
    sel = 1.0  # Unit cell size
    rvar = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1])  # Radii of truss elements
    NC = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])  # Nodal coordinates
    CA = np.array([[1, 2], [2, 3], [3, 4], [4, 1], [1, 3], [2, 4]])  # Connectivity array
    Avar = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])  # Cross-sectional areas
    E = 210e9  # Young's modulus (e.g., steel in Pascals)
    C = np.zeros((3, 3))  # Initially empty stiffness tensor
    sidenum = 2  # Number of nodes along one side of the truss grid



    # Call the generateC function
    C_updated2, uBasket2, FBasket2 = generateC(sel, rvar, NC, CA, Avar, E, C, sidenum)

    # Check if the outputs are the same
    # print(np.allclose(C_updated, C_updated2))
    # print('Stiffness 1', C_updated)
    print('Stiffness 2', C_updated2)



    # # Print the outputs
    # print("Updated Stiffness Tensor (C):")
    # print(C_updated)
    # print("\nDisplacement Vectors (uBasket):")
    # print(uBasket)
    # print("\nForce Vectors (FBasket):")
    # print(FBasket)






