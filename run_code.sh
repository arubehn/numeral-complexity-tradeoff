chmod u+x get_data.sh
./get_data.sh

chmod u+x setup.sh
./setup.sh

cd code

python3 generate_complexity.py
Rscript mixture_model.R
Rscript make_graphics.R
