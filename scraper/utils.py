members = '''
Bajbak	Maciej
Bajeński	Dariusz
Barwiński	Leszek
Ciesielski	Jan
Dąbrowska	Joanna
Deperas	Aleksander
Dębicki	Maciej
Smoleń	Agnieszka
Dudkowiak	Michał
Frączyk	Jarosław
Frączyk	Anna
Frąk	Edyta
Godlewski	Krzysztof
Gołębiewski	Michał
Górski	Michał
Hussein	Anna
Hussein	Abdalla
Jabłońska	Magdalena
Jabłoński	Dominik
Janeczko	Katarzyna
Janiszewski	Dariusz
Jaworski	Jarosław
Kaczorowska	Anna
Kalinowski	Arkadiusz
Koperski	Sebastian
Kozicki	Roman
Kudła	Agnieszka
Lis	Alicja
Lubiszewski	Robert
Mączka	Zbigniew
Mechliński	Bartłomiej
Miedzak	Dawid
Miedzak	Karol
Olszewski	Karol
Pazderska	Małgorzata
Pietrzak	Marcin
Pniewski	Łukasz
Rok-Szpala	Sylwia
Samerek	Dariusz
Słuniecka	Aleksandra
Słuniecki	Tomasz
Stawarska	Elżbieta
Strzelecki	Mariusz
Syrocka	Agnieszka
Szarwiński	Mariusz
Szymański	Jarosław
Śliwiński	Mariusz
Twarowski	Arkadiusz
Twarowski	Karol
Walkowiak	Krzysztof
Wasieczko	Mateusz
Wawrzynowicz	Sylwester
Wiśniewska	Daniela
Wiśniewski	Marek
Wiśniewski	Jakub
Wojciechowski	Przemysław
Wojciechowski	Sławomir
Wojewoda	Tomasz
Wysocki	Dariusz
Ziółkowski	Grzegorz
Żyłkowska	Krystyna
Mączka	Małgorzata
Krajnik	Magdalena
Klabun	Wojciech
Marchlik-Fisz	Joanna
Wiśniewska	Daniela
Krupska	Karolina
'''
team_members = members.strip().split('\n')
[n.split('\t')[1] + ' ' + n.split('\t')[0] for n in members.strip().split('\n')] + \
 [n.split('\t')[0] + ' ' + n.split('\t')[1] for n in members.strip().split('\n')]

def get_team_member(name):
    if name == 'Edyta Anna FRĄK':
        name = 'Edyta Frąk'
    if name == 'Magda M. JABŁOŃSKA':
        name = 'Magdalena Jabłońska'
    if name == 'Daniela Maria WIŚNIEWSKA':
        name = 'Daniela Wiśniewska'
    for n in team_members:
        f_l = n.split('\t')[1] + ' ' + n.split('\t')[0]
        l_f = n.split('\t')[0] + ' ' + n.split('\t')[1]
        if f_l.lower() == name.lower() or l_f.lower() == name.lower():
            return f_l

def gender_icon(g):
    return '🏃🏻' if g == 'M' else '🏃‍♀️'


def get_award(position):
    if position == 1:
        return 'OPEN 🥇'
    if position == 2:
        return 'OPEN 🥈'
    if position == 3:
        return 'OPEN 🥉'
    return ''

def get_cat_award(position):
    if position == 1:
        return 'kat. 🥇'
    if position == 2:
        return 'kat. 🥈'
    if position == 3:
        return 'kat. 🥉'
    return ''
