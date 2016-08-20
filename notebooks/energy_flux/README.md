The IPython Notebooks in this directory are made by Nancy for
quick sharing of results. The notebooks and script have to do with energy flux.

The links below are to static renderings of the notebooks via
[nbviewer.ipython.org](http://nbviewer.ipython.org/).
Descriptions below the links are from the first cell of the notebooks
(if that cell contains Markdown or raw text).

* ##[Barotropic to baroclinic conversion - development.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/Barotropic to baroclinic conversion - development.ipynb)  
    
    Notebook to develop calculations for barotropic to baroclinic conversion,  
      
    $ C = <p'(-H) \vec{U}\cdot\nabla H>$  
      
    where $p'$ is pressure perturbation, $\vec{U}$ is barotropic velocity, $H$ is bottom topography. So bottom depth is z = -H(x,y)  
      
    $ p' = \int_z^0 N^2\zeta dz' - \frac{1}{H} \int_{-H}^0 \int_z^0 N^2\zeta dz' dz$  
      
    and $\zeta$ is isopycncal displacement. $<>$ denote an average over a tidal period. See Carter et al (2008), Energetics of M2 Barotropic to Baroclinic Tidal Conversion at the Hawaiian Islands  
      
    Alternatively, Kelly et al 2010 Internal‐tide energy over topography, defines  
      
    $ p' = p(x,z) - P(x)$  
      
    where $p(x,z)$ is the total pressure and $P(x)$ is the depth-averaged pressure.  
      
    $P(x) = \frac{1}{H}\int_{-H}^0 p(x,z)dz $  
      
    This is bizarre to me because were it the time dependency? I guess, in the model, the depth levels are actually changing with time, so both $z$ and $dz$ are time dependent.   
      
    I will use the Kelly et al 2010 apporach. Note, Kelly warns of using $C_S$ as a correction in shallow areas.  

* ##[JDF energy fluxes.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/JDF energy fluxes.ipynb)  
    
    This is a notebook for developing energy flux calculations.  

* ##[Victoria energy flux.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/Victoria energy flux.ipynb)  
    
    This is a notebook for developing energy flux calculations.  

* ##[BP energy flux.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/BP energy flux.ipynb)  
    
    This is a notebook for developing energy flux calculations.  

* ##[Barotropic energy flux - total.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/Barotropic energy flux - total.ipynb)  
    
    Check against Parker's calculations.  
      
    The formula I use is:  
    $  
    Energy flux = \rho_0*g*<(\int v_{barotropic}(t,x)*H(x)*\eta(t,x)*dx))>  
    $  
      
    where $H$ is depth of a water column, $\eta$ is sea surface height, $v_{barotropic}$ is depth-averaged $y$ current, $g$ is acceleration due to gravity, $\rho_0$ is a reference density (1035 kg/m$^3$), and $<>$ represents a time average  

* ##[Develop energy flux calculations.ipynb](http://nbviewer.ipython.org/urls/bitbucket.org/salishsea/analysis-nancy/raw/tip/notebooks/energy_flux/Develop energy flux calculations.ipynb)  
    
    This is a notebook for developing energy flux calculations.  


##License

These notebooks and files are copyright 2013-2016
by the Salish Sea MEOPAR Project Contributors
and The University of British Columbia.

They are licensed under the Apache License, Version 2.0.
http://www.apache.org/licenses/LICENSE-2.0
Please see the LICENSE file for details of the license.
