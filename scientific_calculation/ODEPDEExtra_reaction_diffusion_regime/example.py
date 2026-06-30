def reaction_diffusion_regime(diffusion, reaction, length_scale):
    if diffusion < 0 or length_scale <= 0:
        raise ValueError("invalid physical parameters")
    if diffusion == 0 and reaction == 0:
        return "inactive"
    if diffusion == 0:
        return "reaction-only"
    damkohler = abs(reaction) * length_scale * length_scale / diffusion
    if damkohler < 0.1:
        return "diffusion-dominated"
    if damkohler > 10:
        return "reaction-dominated"
    if reaction < 0:
        return "decay-balanced"
    return "growth-balanced"
