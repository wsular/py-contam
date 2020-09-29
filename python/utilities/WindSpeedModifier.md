# Summary of Equations related to Wind Speed Modifier
- Von P. Walden, 23 April 2020
- Derived from [CONTAM User Manual](https://nvlpubs.nist.gov/nistpubs/TechnicalNotes/NIST.TN.1887.pdf)

---

## Start with the definition of the Pressure Coefficient

$$ P_w = \frac{\rho V_H^2}{2} C_p $$

$$ C_p = \frac{2 P_w}{\rho V_H^2} $$

$$ C_h f(\theta) = \frac{2 P_w}{\rho V_H^2}$$

$$ C_h = \frac{2 P_w}{\rho V_H^2 f(\theta)}$$

Note that $P_w$ and $\rho V_H^2$ have the same units; pressure. Therefore, $C_p$, $C_h$ and $f(\theta)$ are dimensionless. In fact, $C_p$ is a well known parameter in fluid dynamics called the pressure coefficient. As defined in the CONTAM User Manual, the Wind Speed Modifier $(C_h)$ is a dimensionless number that accounts "for terrain and elevation effects", while $f(\theta)$ is an additional dimensionless "function of the relative wind direction". Note that $\theta \equiv \theta_w - \theta_s$, which is the angle between the wind direction and the normal to the surface (wall) of the building under consideration.

---
## Now consider the Wind Speed Modifier

Equation 1 in the CONTAM User Manual defines $C_h$ as

$$ C_h =  \frac{V_H^2}{V_{met}^2} = A_o^2 \left( \frac{H}{H_{met}} \right) ^{2a} $$

Note that because $C_h$ is dimensionless, so is $A_o$. So both cofficients $A_o$ and $a$ are dimensionless parameters that relate to the ratio of velocities at the top of the building wall to the velocity that is actually measured by the meteorological sensor. Therefore, both $A_o$ and $a$ depend on the structure of the wind in the boundary layer.

---
## Wind in the Boundary Layer

The discussion about the various velocites in the CONTAM User Manual is a bit confusing. The manual lists four different velocities: $V_o$, $V$, $V_{met}$ and $V_H$. $V_o$ is the velocity at the building site, but at the same level as $V_{met}$, which is typically the velocity at a nearby airport or some official meteorological observatory. $V_H$ is the velocity at height $H$, which is the top of the building wall. I believe that $V$ is an arbitrary velocity and that the equation

$$ V_o = A_o V$$

simply shows how to scale velocities that are measured at the same place, but at different heights.

Using this same height scaling, the CONTAM User Manual gives two equations for $V_H$, which is the quantity we want:

$$ V_H = V_o \left( \frac{H}{H_{met}} \right)^a $$

and

$$ V_H = V_{met} \left( \frac{\delta_{met}}{H_{met}} \right)^{a_{met}}  \left( \frac{H}{\delta} \right)^a$$

By setting these equations equal to each other, we get

$$ V_o \left( \frac{H}{H_{met}} \right)^a = V_{met} \left( \frac{\delta_{met}}{H_{met}} \right)^{a_{met}}  \left( \frac{H}{\delta} \right)^a$$

and we can solve for $V_o$ as a function of $V_{met}$.

$$ V_o = V_{met} \left( \frac{\delta_{met}}{H_{met}} \right)^{a_{met}}  \left( \frac{H_{met}}{\delta} \right)^a \left( \frac{H_{met}}{H} \right)^a$$

which gives

$$ V_o = V_{met} \left( \frac{\delta_{met}}{H_{met}} \right)^{a_{met}}  \left( \frac{H_{met}}{\delta} \right)^a $$

This yields the same equation for $A_o$ that is in the CONTAM User Manual (bottom of page 151)

$$ A_o = \left( \frac{\delta_{met}}{H_{met}} \right)^{a_{met}}  \left( \frac{H_{met}}{\delta} \right)^a $$

**But the key point for our experiments is that,**

$$ V_o = V_{met} $$

**or equivalently**

$$ \delta_{met} = \delta $$

This is because we made our own meteorological measurements at the study home sites. This reduces the equation above to 

$$ A_o = 1 $$

for our study homes. This is the same value for $A_o$ for an airport, the site where typically measurements are acquired from.

---
## Summary
**So I don't think we should be adjusting the value of $A_o$ for our experiments, but rather selecting an appropriate value for $a$.**

1. The value of $a$ tells us how to relate our on-site meteorological measurements at $H_{met}$ to the height of the building wall $H$.
2. Because $A_o = 1$, the Wind Speed Modifier reduces to 

$$ C_h = \left( \frac{H}{H_{met}} \right) ^{2a} $$

which depends of the choice of $a$.

3. Note also that $V_H$ is now given by

$$ V_H = V_{met} \left( \frac{H}{H_{met}} \right) ^a $$

when $A_o = 1$.

4. It also may be important that $C_h$ also depends on the wind pressure profile $f(\theta)$, so we might need to pay more attention to that parameter. Note that

$$ C_h = \frac{2 P_w}{\rho V_H^2 f(\theta)} =  \frac{V_H^2}{V_{met}^2} = A_o^2 \left( \frac{H}{H_{met}} \right) ^{2a} $$

so

$$ f(\theta) = \frac{2 P_w}{\rho V_H^2} \left( \frac{H_{met}}{H} \right) ^{2a} = \frac{2 P_w}{\rho V_{met}^2}$$
