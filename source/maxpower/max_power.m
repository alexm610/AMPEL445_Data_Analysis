function []=max_power(folder)
    matfiles = dir([folder '/*.mat']);
    number_of_files = length(matfiles);  
    file_count = 0;
    for i = 1:number_of_files
        matfile = [folder '/' matfiles(i).name]
        file=load(matfile);
        data=file.scandata;
        fibre1_power=data.power(:,1); 
        fibre3_power=data.power(:,2);
        fibre4_power=data.power(:,3);
        wavelength=data.wavelength;

        datapoints=length(data.power)

        lambda1 = 0;
        lambda3 = 0;
        lambda4 = 0;
        max1 = -100;
        max3 = -100;
        max4 = -100;
        for i = 1:datapoints
            if fibre1_power(i,1) >= max1
                max1 = fibre1_power(i,1);
                lambda1 = wavelength(i);
            else 
                ;
            end
            if fibre3_power(i,1) >= max3
                max3 = fibre3_power(i,1);
                lambda3 = wavelength(i);
            else 
                ;
            end
            if fibre4_power(i,1) >= max4
                max4 = fibre4_power(i,1);
                lambda4 = wavelength(i);
            else 
                ;
            end
        end

        max1
        lambda1
        max3
        lambda3
        max4
        lambda4
        file_count = file_count + 1;
    end
    file_count
end
