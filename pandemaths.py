#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
"""
PandeMaths - 2020 - by psy (epsylon@riseup.net)

You should have received a copy of the GNU General Public License along
with PandeMaths; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
VERSION = "v0.4_beta"
RELEASE = "02042020"
SOURCE1 = "https://code.03c8.net/epsylon/pandemaths"
SOURCE2 = "https://github.com/epsylon/pandemaths"
CONTACT = "epsylon@riseup.net - (https://03c8.net)"

pandemic_model_variables_path = "model/pandemia.txt" # pandemia variables file
extended_model_variables_path = "model/extended.txt" # extended model variables file
simulation_templates_path = "templates/" # templates files
reports_path = "reports/" # reports files

import json, datetime, os, random, sys
import matplotlib.pyplot as plt

def model_maths():
    print("[Info] Reviewing Model ...\n")
    try:
        print(" "+"-"*5+"\n")
        f = open(pandemic_model_variables_path, "r")
        model_variables = f.readlines()
        f.close()
        for v in model_variables:
            print("   - "+str(v.replace("\n", "")))
    except:
        pass
    try:
        print("\n "+"-"*5+"\n")
        f = open(extended_model_variables_path, "r")
        extended_variables = f.readlines()
        f.close()
        for v in extended_variables:
            print("   - "+str(v.replace("\n", "")))
    except:
        pass
    print("\n "+"-"*5+"\n")

def simulation():
    print("[Info] Defining ecosystem ...\n")
    total_population = input("   + Total population (default: 100000): ")
    try:
        total_population = int(total_population)
    except:
        total_population = 100000
    if not total_population:
        total_population = 100000
    starting_population = total_population
    infected_starting = input("   + Infected (at the beginning) population (default: 1): ")
    try:
        infected_starting = int(infected_starting)
    except:
        infected_starting = 1
    if not infected_starting or infected_starting < 1:
        infected_starting = 1
    infected = infected_starting
    print("\n "+"-"*5+"\n")
    print("[Info] Establishing time units ...\n")
    days = input("   + Number of days (default: 200): ")
    try:
        days = int(days)
    except:
        days = 200
    if not days:
        days = 200
    daily_rate_interaction = input("   + Daily rate of interaction between individuals (default: 2.50): ")
    try:
        daily_rate_interaction = int(daily_rate_interaction)
    except:
        daily_rate_interaction = 2.50
    if not daily_rate_interaction:
        daily_rate_interaction = 2.50
    print("\n "+"-"*5+"\n")
    template = input("+ CHOOSE: (O)pen Simulation or (L)oad template: ").upper()
    if template == "O": # New Simulation
        average_rate_duration = None
        probability_of_contagion = None
        recovery_rate = None
        simulation_name = "OPEN"
        new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population)
    else: # Load template
        load_template(total_population, infected_starting, days, daily_rate_interaction, starting_population)

def load_template(total_population, infected_starting, days, daily_rate_interaction, starting_population):
    print("\n "+"-"*5+"\n")
    print("[Info] Generating templates ...\n")
    import glob
    templates = {}
    i = 0
    for file in glob.iglob(simulation_templates_path + '*', recursive=False):
        if(file.endswith(".txt")): 
            i = i +1
            f=open(file, 'r')  
            template =  f.read().replace('\n',' ')
            templates[i] = file.replace("templates/",""), template.upper() # add template to main dict
            f.close()
    for k,v in templates.items():
        print ("  ["+str(k)+"] - "+str(v[0].replace(".txt","")))
    print("\n "+"-"*5+"\n")
    template_set = input("+ CHOOSE: Number of template (ex: 1): ").upper()
    try:
        template_set = int(template_set)
    except:
        template_set = 1
    if not template_set or template_set > len(templates) or template_set < 1:
        template_set = 1
    for k,v in templates.items():
        if template_set == k:
            simulation_name = v[0].replace(".txt","")
            average_rate_duration = int(v[1].split("DURATION:")[1].split(" ")[0])
            probability_of_contagion = int(v[1].split("CONTAGION:")[1].split(" ")[0])
            recovery_rate = int(v[1].split("RECOV:")[1].split(" ")[0])
            new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population)

def new_simulation(total_population, infected_starting, days, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, simulation_name, starting_population):
    print("\n "+"-"*5+"\n")
    print("[Info] Generating variables ...\n")
    if average_rate_duration == None:
        average_rate_duration = input("   + Average duration of illness (default: 12) (days): ")
        try:
            if average_rate_duration == 0:
                pass
            else:
                average_rate_duration = int(average_rate_duration)
        except:
            average_rate_duration = 12
        if average_rate_duration < 0 or average_rate_duration > 100:
            average_rate_duration = 12
    else:
        print("   + Average duration of illness: "+str(average_rate_duration)+" days")
    if probability_of_contagion == None:
        probability_of_contagion = input("   + Infection rate (default: 14%): ")
        try:
            if probability_of_contagion == 0:
                pass
            else:
                probability_of_contagion = int(probability_of_contagion)
        except:
            probability_of_contagion = 14
        if probability_of_contagion < 0 or probability_of_contagion > 100:
            probability_of_contagion = 14
    else:
        print("   + Infection rate: "+str(probability_of_contagion)+"%")
    if recovery_rate == None:
        recovery_rate = input("   + Recovery rate (default: 95%): ")
        try:
            if recovery_rate == 0:
                pass
            else:
                recovery_rate = int(recovery_rate)
        except:
            recovery_rate = 95
        if recovery_rate < 0 or recovery_rate > 100:
            recovery_rate = 95
    else:
        print("   + Recovery rate: "+str(recovery_rate)+"%")
    mortality = 100 - recovery_rate
    print("\n "+"-"*5+"\n")
    print("[Info] Building parameters ...\n")
    print("   + Mortality rate: "+str(mortality)+"%")
    mortality = mortality / 100
    recovery_rate = recovery_rate / 100
    probability_of_contagion = probability_of_contagion / 100
    infected = infected_starting
    susceptible_starting = int(total_population) - int(infected)
    susceptible = susceptible_starting # susceptitble at start
    recoveries = 0 # recoveries individuals at start
    print("   + Susceptible: "+str(susceptible))
    print("\n"+"="*50+"\n")
    print("[Info] Launching Simulation: [ "+str(simulation_name)+" ] ...")
    print("\n"+"="*50+"\n")
    current_time = datetime.datetime.now() # current datetime
    if not os.path.exists(reports_path): # create folder for reports
        os.makedirs(reports_path)
    data = {
      'METADATA': [
        {
        'Simulation Name': str(simulation_name),
        'Datetime': str(current_time)
        }
      ],
      'ECOSYSTEM': [
        {
        'Total Population': str(total_population),
        'Infected (at the beginning)': str(infected_starting),
        'Number of days': str(days),
        'Daily rate of interaction between individuals': str(daily_rate_interaction),
        'Average duration of illness': str(average_rate_duration),
        'Infection rate': str(probability_of_contagion*100)+"%",
        'Recovery rate': str(recovery_rate*100)+"%",
        'Mortality': str(mortality*100)+"%",
        'Susceptible': str(susceptible),
        }
      ],
     'SIMULATION': [
        {}
      ]
    }
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".txt"), 'a', encoding='utf-8') as f: # append into txt
        f.write("="*50+os.linesep)
        f.write("Simulation Name:"+str(simulation_name)+os.linesep)
        f.write("Infected (at the beginning):"+str(infected_starting)+os.linesep)
        f.write("Number of days:"+str(days)+os.linesep)
        f.write("Daily rate of interaction between individuals:"+str(daily_rate_interaction)+os.linesep)
        f.write("Average duration of illness:"+str(average_rate_duration)+os.linesep)
        f.write("Infection rate:"+str(probability_of_contagion*100)+"%"+os.linesep)
        f.write("Recovery rate:"+str(recovery_rate*100)+"%"+os.linesep)
        f.write("Mortality:"+str(mortality*100)+"%"+os.linesep)
        f.write("Susceptible:"+str(susceptible)+os.linesep)
        f.write("="*50+os.linesep)
    entire_population_infected = 0
    plot_starting_population = []
    plot_days = []
    plot_contagion = []
    plot_recoveries = []
    plot_deaths = []
    plot_susceptible = []
    plot_infected = []
    plot_total_population = []
    plot_total_contagion = []
    plot_total_recovered = []
    plot_total_deceased = []
    entire_population_infected = False
    average_end_duration = 1
    infected_resolving_situation = False
    for i in range(0, days):
        if i > 0:
            try:
                status_rate = round(int(infected*100/total_population))
            except:
                status_rate = 100
            if status_rate < 11: # ENDEMIA (-11%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: [ ENDEMIC! ]"
                else:
                    if int(total_deceased*100/starting_population) > 49:
                        status = "IMPACT LEVEL: VACCINED! [ ERRADICATED BUT AT LEAST HALF OF THE POPULATION HAS DIED! ]"
                    else:
                        status = "IMPACT LEVEL: VACCINED! [ ERRADICATED! ]"
            elif status_rate > 10 and status_rate < 25: # EPIDEMIA (>10%<25%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: [ EPIDEMIC! ]"
                else:
                    status = "IMPACT LEVEL: [ FOCUS OF INCUBATION! ]"
            else: # PANDEMIA (>25%)
                if susceptible > 0:
                    status = "IMPACT LEVEL: [ PANDEMIC! ]"
                else:
                    status = "IMPACT LEVEL: [ MOSTLY INCUBATING! ]"
            sir = susceptible+infected+recoveries # S-I-R model
            try:
                contagion = round(infected*daily_rate_interaction*susceptible/sir*probability_of_contagion) # contagion rounded rate
            except:
                contagion = 100
            recoveries = int(infected*recovery_rate/average_rate_duration) # recoveries rounded rate
            deaths = int(infected*mortality/average_rate_duration) # deaths rounded rate
            susceptible = int(susceptible - contagion + recoveries - deaths)
            infected = int(infected+contagion-recoveries-deaths)
        else: # related to the first day
            status = "[ SIMULATION START! ]"
            contagion = 0
            recoveries = 0
            deaths = 0
            total_recovered = 0
            total_deceased = 0
            susceptible = total_population - infected
            total_contagion = infected_starting
        total_contagion = total_contagion + contagion
        total_deceased = total_deceased + deaths
        total_population = total_population - total_deceased
        total_recovered = total_recovered + recoveries
        if total_recovered > starting_population:
            total_recovered = total_population
        print("-"*75+"\n")
        if total_population > 0: # some population still alive
            if contagion == 0 and recoveries == 0 and deaths == 0 and total_population != starting_population: # no more interactions after starting
                status = "IMPACT LEVEL: [ INFECTED RESOLVING THEIR SITUATION! ]"
                if infected == 0: # no more interactions + max average_rate_duration -> end!
                    print("="*50+"\n")
                    report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
                    export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                    export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                    export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                else:
                    infected_resolving_situation = True
                    average_end_duration = average_end_duration + 1
                    if average_end_duration < average_rate_duration:
                        res = random.randrange(2)
                        if res == 1: # more recoveries!
                            res_rec = random.randrange(infected)
                            recoveries = res_rec
                            deaths = infected - recoveries
                        else: # more deaths!
                            res_dea = random.randrange(infected)
                            deaths = res_dea
                            recoveries = infected - deaths
                        infected = 0
                        report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
                        export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                        export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                        export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                break
            if total_contagion >= starting_population: # all are infected
                total_contagion = starting_population
                susceptible = 0
                if entire_population_infected == False: # adding output markers to this event
                    infected = total_population
                    print("="*50+"\n")
                    status = "IMPACT LEVEL: [ THE ENTIRE POPULATION IS INFECTED! ]"
                    report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
                    export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                    export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                    export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased) 
                    entire_population_infected = True
                    print("="*50+"\n")
                else:
                    if infected_resolving_situation == False:
                        status = "IMPACT LEVEL: [ SOME POPULATION IS INCUBATING! ]"
                        report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased) 
                        export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased) 
                        export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                        export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
            else: # more population susceptible than infected
                report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
                export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
                export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased) 
        else: # no more population exposed
            total_population = 0
            contagion = 0
            susceptible = 0
            recoveries = 0
            deaths = 0
            if int(susceptible) > 0 and int(infected) > 0: # some have survived
                status = "IMPACT LEVEL: VACCINED! [ BUT WITH MANY CASUALTIES! ]"
            else: # no survivors!
                status = "IMPACT LEVEL: [ INFECTED RESOLVING THEIR SITUATION! ]"
                infected_resolving_situation = True
                average_end_duration = average_end_duration + 1
                if average_end_duration < average_rate_duration:
                    res = random.randrange(2)
                    if res == 1: # more recoveries!
                        res_rec = random.randrange(infected)
                        recoveries = res_rec
                        deaths = infected - recoveries
                    else: # more deaths!
                        res_dea = random.randrange(infected)
                        deaths = res_dea
                        recoveries = infected - deaths
                    infected = 0
            print("="*75+"\n")
            report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
            export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased) 
            export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased) 
            export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
            break
    print("="*50+"\n")
    status = "[ SIMULATION END! ]"
    i = i + 1
    contagion = 0
    recoveries = 0
    deaths = 0
    susceptible = 0
    infected = 0
    report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased)
    export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
    export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
    export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased)
    generate_graph(starting_population, simulation_name, infected_starting, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, mortality, total_population, plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time) # generate final graph
    print("="*75+"\n")
    print ("[Info] [REPORTS] (txt|json|png) -> [SAVED!] at: '"+str(reports_path+"PandeMaths-report_"+str(current_time)+"/'")+"\n")

def extract_rates_current_day(starting_population, total_population, contagion, recoveries, deaths, total_contagion, total_recovered, total_deceased, infected, susceptible):
    try:
        rate_contagion = "%0.2f" % ((contagion/total_population)*100)
    except:
        rate_contagion = 0.00
    try:
        rate_recoveries = "%0.2f" % ((recoveries/infected)*100)
    except:
        rate_recoveries = 0.00
    try:
        rate_deaths = "%0.2f" % ((deaths/infected)*100)
    except:
        rate_deaths = 0.00
    try:
        rate_total_contagion = "%0.2f" % ((total_contagion/starting_population)*100)
    except:
        rate_total_contagion = 0.00
    try:
        rate_total_recovered = "%0.2f" % ((total_recovered/starting_population)*100)
    except:
        rate_total_recovered = 0.00
    try:
        rate_total_deceased = "%0.2f" % ((total_deceased/starting_population)*100)
    except:
        rate_total_deceased = 0.00
    try:
        rate_final_population = (starting_population-total_deceased)*100/starting_population
    except:
        rate_final_population = 0.00
    try:
        rate_infected = "%0.2f" % ((infected/total_population)*100)
    except:
        rate_infected = 0.00
    try:
        rate_susceptible = "%0.2f" % ((susceptible/total_population)*100)
    except:
        rate_susceptible = 0.00
    if rate_recoveries == 0 and rate_deaths == 0:
        if recoveries > 0 or deaths > 0:
            total_alive = recoveries + deaths
            if recoveries > 0:
                rate_recoveries = "%0.2f" % (recoveries*100/total_alive)
            if deaths > 0:
                rate_deaths = "%0.2f" % (deaths*100/total_alive)
    return rate_contagion, rate_recoveries, rate_deaths, rate_total_contagion, rate_total_recovered, rate_total_deceased, rate_final_population, rate_infected, rate_susceptible

def report_current_day(i, status, contagion, total_population, recoveries, deaths, susceptible, infected, starting_population, total_contagion, total_recovered, total_deceased):
    if susceptible > total_population:
        susceptible = total_population
    if infected > starting_population:
        infected = starting_population
    rate_contagion, rate_recoveries, rate_deaths, rate_total_contagion, rate_total_recovered, rate_total_deceased, rate_final_population, rate_infected, rate_susceptible = extract_rates_current_day(starting_population, total_population, contagion, recoveries, deaths, total_contagion, total_recovered, total_deceased, infected, susceptible) # extract current daily rates
    print("  -> [DAY: "+str(i)+"]\n")
    print("    -> Contagion: ("+str(int(contagion))+")["+str(rate_contagion)+"%] - [ Recoveries: ("+str(int(recoveries))+")["+str(rate_recoveries)+"%] - Deaths: ("+str(int(deaths))+")["+str(rate_deaths)+"%] ]\n")
    print("     -> Status: "+str(status))
    print("        * Total Population: ("+str(int(starting_population)-int(total_deceased))+"/"+str(starting_population)+")["+str(int(rate_final_population))+"%] - [ Susceptible: ("+str(int(susceptible))+")["+str(rate_susceptible)+"%] - Infected: ("+str(int(infected))+")["+str(rate_infected)+"%] ]")
    print("        * Total Contagion: ("+str(int(total_contagion))+")["+str(rate_total_contagion)+"%] - Total Recovered: (" +str(int(total_recovered))+")["+str(rate_total_recovered)+"%] - Total Deceased: ("+str(int(total_deceased))+")["+str(rate_total_deceased)+"%]\n")

def export_to_txt(current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased):
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".txt"), 'a', encoding='utf-8') as f: # append into txt
        f.write(os.linesep)
        f.write("Day:"+str(i)+os.linesep)
        f.write("Status:"+str(status)+os.linesep)
        f.write("Contagion:"+str(contagion)+os.linesep)
        f.write("Recoveries:"+str(recoveries)+os.linesep)
        f.write("Deaths:"+str(deaths)+os.linesep)
        f.write("Susceptible:"+str(susceptible)+os.linesep)
        f.write("Infected:"+str(infected)+os.linesep)
        f.write("Total Population:"+str(total_population)+os.linesep)
        f.write("Total Contagion:"+str(total_contagion)+os.linesep)
        f.write("Total Recovered:"+str(total_recovered)+os.linesep)
        f.write("Total Deceased:"+str(total_deceased)+os.linesep)

def export_to_json(data, current_time, i, status, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased):
    data['SIMULATION'][0]['DAY'] = str(i)
    data['SIMULATION'][0]['Status'] = str(status)
    data['SIMULATION'][0]['Contagion'] = str(int(contagion))
    data['SIMULATION'][0]['Recoveries'] = str(int(recoveries))
    data['SIMULATION'][0]['Deaths'] = str(int(deaths))
    data['SIMULATION'][0]['Susceptible'] = str(int(susceptible))
    data['SIMULATION'][0]['Infected'] = str(int(infected))
    data['SIMULATION'][0]['Total Population'] = str(int(total_population))
    data['SIMULATION'][0]['Total Contagion'] = str(int(total_contagion))
    data['SIMULATION'][0]['Total Recovered'] = str(int(total_recovered))
    data['SIMULATION'][0]['Total Deceased'] = str(int(total_deceased))
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    with open(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".json"), 'a', encoding='utf-8') as f: # append into json
        json.dump(data, f, ensure_ascii=False, sort_keys=False, indent=4)

def export_to_graph(plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time, starting_population, i, contagion, recoveries, deaths, susceptible, infected, total_population, total_contagion, total_recovered, total_deceased):
    plot_starting_population = starting_population
    plot_days.append(i)
    plot_contagion.append(contagion)
    plot_recoveries.append(recoveries)
    plot_deaths.append(deaths)
    plot_susceptible.append(susceptible)
    plot_infected.append(infected)
    plot_total_population.append(total_population)
    plot_total_contagion.append(total_contagion)
    plot_total_recovered.append(total_recovered)
    plot_total_deceased.append(total_deceased)

def generate_graph(starting_population, simulation_name, infected_starting, daily_rate_interaction, average_rate_duration, probability_of_contagion, recovery_rate, mortality, total_population, plot_starting_population, plot_days, plot_contagion, plot_recoveries, plot_deaths, plot_susceptible, plot_infected, plot_total_population, plot_total_contagion, plot_total_recovered, plot_total_deceased, current_time):
    plt.plot(plot_days, plot_contagion, "blue", label="Contagion")
    plt.plot(plot_days, plot_recoveries, "grey", label="Recoveries")
    plt.plot(plot_days, plot_deaths, "orange", label="Deaths")
    plt.plot(plot_days, plot_susceptible, "cyan", label="Susceptible")
    plt.plot(plot_days, plot_infected, "purple", label="Infected")
    plt.plot(plot_days, plot_total_population, "pink", label="Total Population")
    plt.plot(plot_days, plot_total_contagion, "red", label="Total Contagion")
    plt.plot(plot_days, plot_total_recovered, "yellow", label="Total Recovered")
    plt.plot(plot_days, plot_total_deceased, "black", label="Total Deceased")
    plt.plot(plot_starting_population)
    plt.title("SIMULATION: '"+str(simulation_name)+"' = Av_Ill: ["+str(average_rate_duration)+" days] - Inf_R: ["+str(probability_of_contagion*100)+"%] - Rec_R: ["+str(recovery_rate*100)+"%] - Mort: ["+str(mortality*100)+"%]\n\nTotal Population: ["+str(total_population)+"/"+str(starting_population)+"] - Infected (at the beginning): ["+str(infected_starting)+"] - Interaction (rate): ["+str(daily_rate_interaction)+"]\n")
    plt.xlabel('Day(s)')
    plt.ylabel('Individual(s)')
    plt.legend(loc='center left', fancybox=True, bbox_to_anchor=(1, 0.5))
    if not os.path.exists(reports_path+"PandeMaths-report_"+str(current_time)): # create folder for reports
        os.makedirs(reports_path+"PandeMaths-report_"+str(current_time))
    plt.savefig(reports_path+"PandeMaths-report_"+str(current_time)+"/"+str("PandeMaths-report_"+str(current_time)+".png"), bbox_inches='tight')

def print_banner():
    print("\n"+"="*50)
    print(" ____                 _      __  __       _   _         ")
    print("-  _ \ __ _ _ __   __- - ___-  \/  - __ _- -_- -__  ___ ")
    print("- -_) / _` - '_ \ / _` -/ _ \ -\/- -/ _` - __- '_ \/ __--2020")
    print("-  __/ (_- - - - - (_- -  __/ -  - - (_- - -_- - - \__ /")
    print("-_-   \__,_-_- -_-\__,_-\___-_-  -_-\__,_-\__-_- -_-___/-by psy")
    print('\n"Pandemics Extensible Mathematical Model"')
    print("\n"+"-"*15+"\n")
    print(" * VERSION: ")
    print("   + "+VERSION+" - (rev:"+RELEASE+")")
    print("\n * SOURCES:")
    print("   + "+SOURCE1)
    print("   + "+SOURCE2)
    print("\n * CONTACT: ")
    print("   + "+CONTACT+"\n")
    print("-"*15+"\n")
    print("="*50)

# sub_init #
print_banner() # show banner
try:
    option = input("\n+ CHOOSE: (M)odel or (S)imulation: ").upper()
except:
    print("\n"+"="*50 + "\n")
    print ("[Info] Try to run the tool with Python3.x.y... (ex: python3 pandemaths) -> [EXITING!]\n")
    sys.exit()
print("")
print("="*50+"\n")
if option == "S": # simulation
    simulation()
else: # model
    model_maths()
print ("="*50+"\n")
