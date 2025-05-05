import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

oscar = pd.read_csv('data/the_oscar_award.csv', sep=',', encoding='latin-1')

# 1. Quais são os filmes mais premiados da história?
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

# 2. Quais diretores receberam mais indicações ao Oscar e quantas vezes venceram?
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

# 3. Quais diretores receberam mais vitórias ao Oscar?
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

# 4. Quem são os atores indicados com mais vitórias?​
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
    
# 5. Quais filmes tiveram mais indicações sem nunca vencer?
def most_nominated_without_wins(n):
    nominations = oscar.groupby('film').size().reset_index(name='nominations')
    wins = (
        oscar[oscar['winner'] == True]
        .groupby('film')
        .size()
        .reset_index(name='wins')
    )
    film_stats = pd.merge(nominations, wins, on='film', how='left').fillna({'wins': 0})
    no_wins = film_stats[film_stats['wins'] == 0].sort_values(by='nominations', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(no_wins['film'].head(n), no_wins['nominations'].head(n), color='violet')
    plt.xlabel('Número de Indicações')
    plt.title('Filmes mais indicados sem nunca vencer')
    plt.gca().invert_yaxis()
    plt.show()

    return no_wins.head(n)

# 6. Quais filmes têm número de indicações acima da média geral de indicações por filme?
def films_above_average(n):
    nominations = oscar.groupby('film').size().reset_index(name='nominations')
    counts = nominations['nominations'].to_numpy()
    avg = np.mean(counts)
    df = nominations[nominations['nominations'] > avg].sort_values('nominations', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(df['film'].head(n), df['nominations'].head(n), color='coral')
    plt.xlabel('Número de Indicações')
    plt.title(
        f'\nOs filmes com indicações acima da média({avg:.2f}):'
    )
    plt.gca().invert_yaxis()
    plt.show()

    return df.head(n)

# 7. Quais foram os artistas mais indicados que nunca venceram um Oscar?
def most_nominated_artists_without_wins(n):
    nominations = oscar.groupby('name').size().reset_index(name='nominations')
    wins = (
        oscar[oscar['winner'] == True]
        .groupby('name')
        .size()
        .reset_index(name='wins')
    )
    artist_stats = pd.merge(nominations, wins, on='name', how='left').fillna({'wins': 0})
    no_wins = artist_stats[artist_stats['wins'] == 0].sort_values('nominations', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(no_wins['name'].head(n), no_wins['nominations'].head(n), color='orchid')
    plt.xlabel('Número de Indicações')
    plt.title('Artistas mais indicados sem nunca vencer um Oscar')
    plt.gca().invert_yaxis()
    plt.show()

    return no_wins.head(n)

# 8. Quais profissionais (atores, atrizes ou diretores) demoraram mais tempo entre a primeira indicação e a primeira vitória?
def professionals_longest_gap(n):
    mask = oscar['category'].str.contains('ACTOR|ACTRESS|DIRECTOR', na=False)
    df_prof = oscar[mask].copy()
    
    df_prof['year_film'] = df_prof['year_film'].astype(int)
    
    first_nom = (
        df_prof
        .groupby('name')['year_film']
        .min()
        .reset_index(name='first_nomination')
    )
    first_win = (
        df_prof[df_prof['winner'] == True]
        .groupby('name')['year_film']
        .min()
        .reset_index(name='first_win')
    )
    
    stats = pd.merge(first_nom, first_win, on='name', how='inner')
    stats['gap_years'] = stats['first_win'] - stats['first_nomination']
    stats = stats.sort_values('gap_years', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(stats['name'].head(n), stats['gap_years'].head(n), color='teal')
    plt.xlabel('Anos entre 1ª indicação e 1ª vitória')
    plt.title('Profissionais com maior intervalo entre indicação e vitória')
    plt.gca().invert_yaxis()
    plt.show()
    
    return stats.head(n)

# 9. Quais profissionais ganharam mais de um Oscar na mesma cerimônia e quantas vezes isso aconteceu?
def professionals_multiple_wins_same_ceremony(n):
    winners = oscar[oscar['winner'] == True].copy()
    wins_per_year = (
        winners
        .groupby(['name', 'year_film'])
        .size()
        .reset_index(name='wins_in_ceremony')
    )
    multi_wins = wins_per_year[wins_per_year['wins_in_ceremony'] > 1]
    count_ceremonies = (
        multi_wins
        .groupby('name')
        .size()
        .reset_index(name='times')
        .sort_values('times', ascending=False)
    )

    plt.figure(figsize=(10, 6))
    plt.barh(count_ceremonies['name'].head(n), count_ceremonies['times'].head(n), color='plum')
    plt.xlabel('Número de Cerimônias com Múltiplas Vitórias')
    plt.title('Profissionais com mais de um Oscar na mesma cerimônia')
    plt.gca().invert_yaxis()
    plt.show()

    return count_ceremonies.head(n)

# 10. Quais profissionais foram indicados em mais categorias diferentes ao longo da carreira?
def professionals_most_diverse_categories(n):
    categories_count = (
        oscar
        .groupby('name')['category']
        .nunique()
        .reset_index(name='num_categories')
    )
    categories_count = categories_count.sort_values('num_categories', ascending=False)

    plt.figure(figsize=(10, 6))
    plt.barh(
        categories_count['name'].head(n),
        categories_count['num_categories'].head(n),
        color='skyblue'
    )
    plt.xlabel('Número de Categorias Distintas')
    plt.title('Profissionais indicados em mais categorias diferentes')
    plt.gca().invert_yaxis()
    plt.show()

    return categories_count.head(n)

# Apresentação dos dados

# 1. Quais são os filmes mais premiados da história?
print("Os filmes mais premiados da história:")
print(most_awarded_movies(5))

# 2. Quais diretores receberam mais indicações ao Oscar e quantas vezes venceram?
print("\nOs diretores mais indicados ao Oscar:")
print(most_nominated_directors(5))

# 3. Quais diretores receberam mais vitórias ao Oscar?
print("\nOs diretores mais vitoriosos no Oscar:")
print(most_winning_directors(5))

# 4. Quem são os indicados com mais vitórias?​
print("\nOs indicados com mais vitórias no Oscar:")
print(most_winning_actors(5))

# 5. Quais filmes tiveram mais indicações sem nunca vencer?
print("\nOs filmes mais indicados sem nunca vencer:")
print(most_nominated_without_wins(5))

# 6. Quais filmes têm número de indicações acima da média geral de indicações por filme?
print(films_above_average(5))

# 7. Quais foram os artistas mais indicados que nunca venceram um Oscar?
print("Artistas mais indicados que nunca venceram o Oscar:")
print(most_nominated_artists_without_wins(5))

# 8. Quais profissionais (atores, atrizes ou diretores) demoraram mais tempo entre a primeira indicação e a primeira vitória?
print("Top profissionais que mais demoraram para converter indicação em vitória:")
print(professionals_longest_gap(5))

# 9. Quais profissionais ganharam mais de um Oscar na mesma cerimônia e quantas vezes isso aconteceu?
print("Profissionais que ganharam mais de um Oscar na mesma cerimônia e quantas vezes isso aconteceu:")
print(professionals_multiple_wins_same_ceremony(5))

# 10. Quais profissionais foram indicados em mais categorias diferentes ao longo da carreira?
print("Profissionais indicados em mais categorias distintas:")
print(professionals_most_diverse_categories(5))