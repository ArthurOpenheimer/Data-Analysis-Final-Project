import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

oscar = pd.read_csv('Data-Analysis-Final-Project/data/the_oscar_award.csv', sep=',', encoding='latin-1')

# Quais são os filmes mais premiados da história?
def most_awarded_movies(n):
    awarded_movies = oscar[oscar['winner'] == True].groupby('film').size().reset_index(name='awards')
    awarded_movies = awarded_movies.sort_values(by='awards', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(awarded_movies['film'].head(n), awarded_movies['awards'].head(n), color='skyblue')
    plt.xlabel('Número de Prêmios')
    plt.title('Filmes mais premiados da história')
    plt.gca().invert_yaxis()
    plt.show()
    
    return awarded_movies.head(n)

# Quais diretores receberam mais indicações ao Oscar e quantas vezes venceram?
def most_nominated_directors(n):
    nominated_directors = oscar[oscar['category'].str.contains('DIRECTOR', na=False)]
    nominated_directors = nominated_directors.groupby('name').size().reset_index(name='nominations')
    nominated_directors = nominated_directors.sort_values(by='nominations', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(nominated_directors['name'].head(n), nominated_directors['nominations'].head(n), color='lightgreen')
    plt.xlabel('Número de Indicações')
    plt.title('Diretores mais indicados ao Oscar')
    plt.gca().invert_yaxis()
    plt.show()
    
    return nominated_directors.head(n)   

def most_winning_directors(n):
    winning_directors = oscar[oscar['winner'] == True].groupby('name').size().reset_index(name='wins')
    winning_directors = winning_directors.sort_values(by='wins', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(winning_directors['name'].head(n), winning_directors['wins'].head(n), color='salmon')
    plt.xlabel('Número de Vitórias')
    plt.title('Diretores mais vitoriosos no Oscar')
    plt.gca().invert_yaxis()
    plt.show()
    
    return winning_directors.head(n)

# Quem são os atores indicados com mais vitórias?​
def most_winning_actors(n):
    winning_actors = oscar[oscar['winner'] == True]
    winning_actors = winning_actors[winning_actors['category'].str.contains('ACTOR|ACTRESS', na=False)]
    winning_actors = winning_actors.groupby('name').size().reset_index(name='wins')
    winning_actors = winning_actors.sort_values(by='wins', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(winning_actors['name'].head(n), winning_actors['wins'].head(n), color='gold')
    plt.xlabel('Número de Vitórias')
    plt.title('Atores mais vitoriosos no Oscar')
    plt.gca().invert_yaxis()
    plt.show()
    
    return winning_actors.head(n)
    
# Apresentação dos dados

# # Quais são os filmes mais premiados da história?
# print("Os filmes mais premiados da história:")
# print(most_awarded_movies(5))

# # Quais diretores receberam mais indicações ao Oscar e quantas vezes venceram?
# print("\nOs diretores mais indicados ao Oscar:")
# print(most_nominated_directors(5))

# print("\nOs diretores mais vitoriosos no Oscar:")
# print(most_winning_directors(5))

# # Quem são os indicados com mais vitórias?​
# print("\nOs indicados com mais vitórias no Oscar:")
# print(most_winning_actors(5))