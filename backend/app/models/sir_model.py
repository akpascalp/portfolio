def sir_step(S, I, R, beta, gamma):
    new_I = beta * S * I
    new_R = gamma * I
    new_S = -new_I
    return S + new_S, I + new_I - new_R, R + new_R

def get_R_value(S: float, I: float):
    S = min(max(S, 0), 1)
    I = min(max(I, 0), 1 - S)
    R = 1 - (S + I)
    return R
