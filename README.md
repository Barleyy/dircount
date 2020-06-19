# Spis treści
1. [Zespół i zakres prac](#zespol)
2. [Wstęp Teoretyczny](#wstęp)
3. [Typy danych](#typy)
4. [Operacje](#operacje)
5. [Komendy](#komendy)
6. [Instrukcja](#instrukcja)

## [Zespół i zakres prac](#zespol)

1. Maciej Nędza - testy, przykładowe programy
2. Wojciech Sałapatek - automatyzacja testów, testy integracyjne
3. Marcin Grzyb - dokumentacja, utilities tworzenia kodu
4. Paweł Gałka - development, features

Wszystkie założenia projektu zostały spełnione. Interpreter został przetestowany automatycznie i manualnie.

## [Wstęp Teoretyczny](#wstęp)

Dircount jest [ezoterycznym językiem programowania](https://en.wikipedia.org/wiki/Esoteric_programming_language). 
Język opiera się na hierarchicznej strukturze katalogów, aby naśladować
strukturę parsowania. Podczas działania programu Foldery zmienne są
przechowywane jako inny zestaw folderów (każdy z nazwą, typem i
wartością), tym razem w folderze appdata użytkownika. Wszystkie
Instrukcje w dircount są zdefiniowane przez liczbę katalogów w aktualnie
rozpatrywanym folderze. Foldery są zczytywane w porządku alfabetycznym.

Celem tej pracy jest skonstruowanie interpretera analizującego język
dirCount w języku programowania Python.

Interpreter jest wolny od elementu lexera, ponieważ sama struktura kodu
jednoznacznie wyznacza tokeny które opisują dany kontekst, element.

Abstract Syntax Tree
--------------------

Aby zrozumieć istotę działania tego języka trzeba zrozumieć koncepcję
AST.

Abstrakcyjne drzewo składniowe (AST), lub po prostu drzewo składniowe,
jest drzewną reprezentacją abstrakcyjnej struktury składniowej kodu
źródłowego napisanego w języku programowania. Każdy węzeł drzewa oznacza
konstrukcję występującą w kodzie źródłowym.

Składnia jest „abstrakcyjna" w tym sensie, że nie reprezentuje każdego
szczegółu występującego w rzeczywistej składni, a jedynie szczegóły
strukturalne lub związane z treścią. Na przykład nawiasy grupujące są
niejawne w strukturze drzewa, więc nie muszą być reprezentowane jako
osobne węzły. Podobnie konstrukcję składniową, taką jak wyrażenie
„warunek-to-wtedy", można określić za pomocą pojedynczego węzła z trzema
rozgałęzieniami.

Odnosząc tą definicję drzewa składniowego do języka dirCount, można
powiedzieć że sama struktura \"kodu\" w języku dirCount jest
zmodyfikowanym drzewem składniowym, gdzie jego budowa nie jest już
abstrakcyjna tylko dokładna w sensie wartości zmiennych, itp. użytych w
kodzie.

Zmianami w stosunku do teoretycznego AST jest też linkowanie węzłów z
liścmi głównie w momencie odnoszenia się referencjami do zmiennych. W
języku dirCount aby odwołać się do zmiennej możemy albo podać jej nazwę,
albo wprost podać miejsce zadeklarowania tej zmiennej odnosząc się do
liścia AST, przez co struktura kodu jest dosyć złożona.

Parser LL
---------

Parser LL to parser czytający tekst od lewej do prawej i produkujący
lewostronne wyprowadzenie metodą zstępującą. Popularne rodzaje parserów
LL to parsery sterowane tablicą i rekurencyjne.

Parsery klasy LL(k) parsują znak po znaku, utrzymując stos zawierający
„spodziewane symbole". Na początku znajdują się tam symbol startowy i
znak końca pliku. Jeśli na szczycie stosu jest ten sam symbol
terminalny, jaki aktualne znajduje się na wejściu, usuwa się go ze
szczytu stosu i przesuwa strumień wejściowy na kolejny znak. Jeśli inny
symbol terminalny zwraca się błąd. Jeśli występuje tam jakiś symbol
nieterminalny, to zdejmuje się go i zależnie od tego symbolu oraz od k
kolejnych znaków wejścia, umieszcza na stosie odpowiedni zestaw symboli.

Parser LL(\*) to lewostronny parser z podglądem dowolnej liczby symboli.

Odnosząc to do języka dirCount schemat interpretera z tematu projektu,
można dość luźno powiązać z działaniem parsera LL(\*) który w trakcie
traversalu wykonuje działania związane z odczytem danych symboli
reprezentowanych przez ilość folderów. Interpreter na danym poziomie
parsingu podgląda od 1 do 2 podfolderów w zależności od kontekstu w
którym się znajduje i wybiera odpowiednie działanie na podstawie
zliczonej ilości podfolderów (np. w procesie declare opisanym w
rozdziale 2, decyduje o typie deklarowanej zmiennej).

Na etapie parsingu każde wywołanie funkcji generuje utworzenie
związanego z danym wywołaniem stosu zmiennych. W momencie każdej
deklaracji, zmiany wartości dokonywanana jest aktualizacja zmiennej
przechowywanej w strukturze słownikowej klucz : wartość = (path, name) =
(value, type).

Gramatyka języka
----------------

Dla interpretera nie używaliśmy pregenerowanych parserów typu ANTLR,
Yacc, Bison ze względu na problem formalizacji gramatyki na oczekiwane
tokeny przez te kompilatory. Język dirCount w założeniu miał być wolny
od kontekstu tekstowego i opierać swoje działanie jedynie na strukturze
drzewiastej swojej reprezentacji kodu.

Poniżej przedstawimy bazowy zarys gramatyki naszego języka, który daje
ogólny pogląd na język dirCount.

1.  Root &#8594; Command

2.  Command &#8594; CommandExpr Command \| epsilon

3.  CommandExpr &#8594; CommandType CommandValue

4.  CommandType &#8594; CommandTypeValue

5.  CommandTypeValue &#8594; function-invoke \| declare \| let \|
    if \| while \| for \| print \| input

6.  CommandValue &#8594; CommandDirFunction1 CommandDirFunction2 \|
    CommandDirDeclare1 CommandDirDeclare2 CommandDirDeclare3 \|
    CommandDirLet1 CommandDirLet2 \| CommandDirWhile1 CommandDirWhile2
    \| CommandDirIf1 CommandDirIf2 CommandDirIf3 \| CommandDirFor1
    CommandDirFor2 CommandDirFor3 CommandDirFor4 \| CommandDirPrint1 \|

7.  CommandDirFunction1 &#8594; FunctionsArgsList

8.  CommandDirFunction2 &#8594; function-path-link

9.  FunctionArgsList &#8594; Element FunctionArgsList \| epsilon

10. CommandDirDeclare1 &#8594; int \| float \| char \| string \|
    boolean \| list \| dict \| function

11. CommandDirDeclare2 &#8594; OperationDir OperationDirVal
    OperationDirVal \| int0 .. int15 \| float0 .. float31 \| boolDir \|
    char0 .. char7 \| string0 string1 \| listDir .. listdir3 \| dictDir
    .. dictDir4 \| function0 function1 function2 function3 function4
    function5

12. function0 &#8594; Command

13. function1 &#8594; Element function1 \| epsilon

14. function2 &#8594; string0 string1

15. string0 &#8594; char0 .. char7

16. listDir &#8594; Element ListDir \| epsilon

17. dictDir &#8594; DirElement DictDir \| epsilon

18. CommandDirDeclare3 &#8594; String0 string1

19. CommandDirLet1 &#8594; LinkDir

20. CommandDirLet2 &#8594;OperationDir OperationDirVal
    OperationDirVal \| int0 .. int15 \| float0 .. float31 \| boolDir \|
    char0 .. char7 \| string0 string1 \| listDir .. listdir3 \| dictDir
    .. dictDir4

21. LinkDir &#8594; link-path \| link-path string0 string1

22. OperationDir &#8594; OperationSubtype OperationSubtypeValue

23. OperationSubtype &#8594; arithmetic \| compare compare \| string
    string string \| list list list list \| dict dict dict dict dict

24. OperationSubtypeValue &#8594; operacje w sekcji

25. OperationValue &#8594; OperationDir OperationDirVal
    OperationDirVal \| int0 .. int15 \| float0 .. float31 \| boolDir \|
    char0 .. char7 \| string0 string1 \| listDir .. listdir3 \| dictDir
    .. dictDir4

26. CommandDirWhile1 &#8594; OperationDir OperationDirVal
    OperationDirVal

27. CommandDirWhile2 &#8594; Command

28. CommandDirIf1 &#8594; boolDir \| OperationDir OperationDirVal
    OperationDirVal

29. CommandDirIf2 &#8594; Command

30. CommandDirIf3 &#8594; epsilon \| Command

31. CommandDirFor1 &#8594; Command \| CommandDirDeclare1
    CommandDirDeclare2 CommandDirDeclare3

32. CommandDirFor2 &#8594; boolDir \| OperationDir OperationDirVal
    OperationDirVal

33. CommandDirFor3 &#8594; Command \| CommandDirLet1 CommandDirLet2

34. CommandDirFor4 &#8594; Command

35. Element &#8594; OperationDir OperationDirVal OperationDirVal \|
    int0 .. int15 \| float0 .. float31 \| boolDir \| char0 .. char7 \|
    string0 string1 \| listDir .. listdir3 \| dictDir .. dictDir4

36. CommandDirPrint1 &#8594; Element CommandDirPrint1 \| epsilon

Foldery boolDir, intDirX, floatDirX, charDirX są postaci bitowej
przyjmując wartość 1 gdy w środku istnieje folder.

Ramowa gramatyka języka dirCount nie jest lewostronnie rekursywna i nie
potrzeba lewostronnej faktoryzacji dlatego translator opiera się o
zmodyfikowane działanie parsera LL(\*)

## [Typy danych](#typy)

Folder typu instrukcji deklaracji zmiennej zawiera informacje o typie
zmiennej.\
W zależności od N(liczba w nawiasie przy nazwie komendy) równemu liczbie
podkatalogów folderu typu dostępne są następujące typy:

-   int(1)

-   float(2)

-   char(3)

-   string(4)

-   boolean(5)

-   list(6)

-   dict(7)

-   function(0)

Podkatalogi wartości zmiennej zawierają w sobie 1 lub 0 podfoledrów -
reprezentują one binarne 1 ( w przypadku obecności katalogu ) i 0 - w
przypadku jego braku

Int
---

Folder wartości zmiennej typu int musi zawierać 16 podfolderów. Pierwszy
podfolder reprezentuje znak (0 dla liczby dodatniej, 1 dla ujemnej),
pozostałe 15 folderów to zapis liczby w postaci binarnej.

Float
-----

Zmienna typu float jest reprezentowana zgodnie ze standardem IEEE
754.Folder wartości zmiennej musi zawierać 32 podfolderów. Pierwszy
podfolder reprezentuje znak (0 dla liczby dodatniej, 1 dla ujemnej), 23
kolejnych folderów zawier wartość mantysy, 8 kolejnych folderów zawiera
wartość cechy.

Char
----

Folder wartości zmiennej typu float musi zawierać 8 podfolderów.
Zawierają one reprezentację zmiennej w kodzie ASCII.

String
------

Folder wartości zmiennej typu String musi zawierać 2 podfoldery.
Pierwszy z nich zawiera katalogi w których zakodowana jest
wartość poszczególnych zmiennych typu char składających się na napis.
Ich wartość jest zakodowana w 8 podfolderach analogicznie jak przy
deklaracji zmiennej typu char. Drugi natomiast pozostaje pusty.

Boolean
-------

Folder wartości zmiennej typu boolean musi zawierać 1 podfolder. Jeśli
zawiera on jeden podfolder, to zmienna przyjmuje wartość true, w
przeciwnym wypadku przyjmuje wartość false.

List
----

Folder wartości zmiennej typu list musi zawierać 4 podfoldery. Pierwszy
z nich zawiera podfoldery przetrzymujące wartości kolejnych elementów
listy.

Dict
----

Folder wartości zmiennej typu dict musi zawierać 5 podfolderów. Pierwszy
z nich zawiera kolejne podfoldery będące elementami słownika. Każdy z
nich musi zawierać 2 podfoldery - pierwszy z nich przetrzymuje wartość
klucza słownika, natomiast drugi zawiera wartość elementu.

Function
--------

Folder funkcji musi zawierać 6 podkatalogów. Pierwszy z nich zawiera
listę wykonywanych przez funkcję, drugi z nich zawiera listę nazw
argumentów przekazywanych do funkcji, trzeci z nich zawiera nazwę
zwracanej zmiennej, w przypadku gdy funkcja ma sygnaturę void folder ten
jest pusty, w przeciwnym wypadku po wykonaniu komand z pierwszego
folderu jest zwracana zmienna z lokalnego stosu zmiennych funkcji.

## [Operacje](#operacje)

W języku dirCount zostały zaimplementowane również operatory:

-   arytmetyczne(1)

-   logiczne(2)

-   operatory dla zmiennych typu String(3)

-   operatory na Listach(4)

-   operatory na Słownikach(5)

Folder operacji musi zawierać 2 podkatalogi:

-   liczba katalogów w pierwszym podkatalogu definiuje typ operatora,
    którego chcemu użyc

-   liczba katalogów w drugim podkatalogu określa konkretny operator z
    danego typu

Operatory arytmetyczne
----------------------

Dostępnymi operatorami arytmetycznymi(które zostały określone poprzez
wartość(N)) są:

-   operator dodawania(1)

-   operator odejmowania(2)

-   operator mnożenia(3)

-   operator dzielenia(4)

-   operator potęgowania(5)

-   operator dzielenia modulo(6)

Operatory logiczne
------------------

Dostępnymi operatorami logicznymi(które zostały określone poprzez
wartość(N)) są:

-   x\<y x\>y(1 oraz 2): logiczne operatory relacji zwracające true gdy
    x jest większy/mniejszy od y

-   x\<=y x\>=y(3 i 4): logiczne operatory relacji zwracające true gdy x
    jest większy lub równy/mniejszy lub równy od y

-   x==y(5): logiczny operator relacji zwracajacy true gdy x i y są
    równe

Operatory dla zmiennych typu String
-----------------------------------

Dla zmiennych typu String dostępnymi operatorami(określonymi poprzez
wartość(N)) są:

-   operator konkatenacji(1)

-   operatory porównania(==,!=)-(2 oraz 3)

Operatory na Listach
--------------------

Operacjami które można zastosować na listach(określonymi poprzez
wartość(N)) są:

-   pobranie elementu z listy(1)

-   łączenie dwoch list(2)

-   dodanie elementu do listy(3)

-   usunięcie elementu na danej pozycji(4)

Operatory na słownikach
-----------------------

Operacjami które można zastosować na słownikach(określonymi poprzez
wartość(N)) są:

-   pobranie elementu ze słownika

-   aktualizacja wartości elementu

-   usunięcie elementu ze słownika

## [Komendy](#komendy)
=======

Folder komendy musi zawierać 2 podkatalogi:

-   liczba katalogów w pierwszym podkatalogu definiuje komendę którą
    chcemy użyć

-   liczba katalogów w drugim podkatalogu zawiera dalsze wyrażenie
    komendy

Dostępne komendy:

- invoke-function (0)
- declare (1)
- if (2)
- let (3)
- while (4)
- for (5)
- print (6)
- input (7)

Declare
-------

Komenda declare pozwala na deklarację zmiennej. Drugi katalog komendy
declare musi zawierać 3 podkatalogi:

-   pierwszy zawiera informacje o typie zmiennej

-   drugi zawiera informacje o wartości zmiennej

-   trzeci zawiera informacje o nazwie zmiennej

If
--

If jest wyrażeniem warunkowym. Jego drugi katalog musi zawierać 2 lub 3
foldery:

-   pierwszy zawiera logiczny warunek

-   drugi zawiera kod wykonywany w przypadku spełnienia warunku

-   trzeci (opcjonalny) zawiera kod wykonywany w przypadku nie
    spełnienia logicznego warunku

Let
---

Let pozwala na zaktualizowanie wartości zmiennej podanej w linku
symbolicznym. Jego drugi katalog musi zawierać 2 foldery:

-   pierwszy przetrzymuje folder linkujący zmienną na 2 sposoby

    -   link do zmiennej

    -   link, foldery stringa z nazwą zmiennej

-   drugi zawiera nową wartość zmiennej

While
-----

While wykonuje instrukcje tak długo jak spełniony jest logiczny warunek.
Jego drugi katalog musi zawierać 2 foldery:

-   pierwszy zawiera logiczny warunek

-   drugi zawiera kod wykonywany tak długo jak spełniony jest warunek

For
---

W zależności od liczby folderów w drugim katalogu komendy zdefiniowane
są różne warianty pętli.

-   W przypadku 1 podfolderu - Nieskończona pętla for, wykonywany jest
    kod z 1 podfolderu

-   W przypadku 3 podfolderów - Pętla z warunkiem i definiowaną zmienną
    iteracyjną:

    -   pierwszy podfolder zawiera deklaracje zmiennej

    -   drugi podfolder zawiera warunek logiczny

    -   trzeci podfolder zawiera kod wykonany w przypadku spełnienia
        warunku

-   W przypadku 4 podfolderów - Pełna pętla for, zawierająca komende
    przypisania wykonywaną pod koniec każdej iteracji

    -   pierwszy podfolder zawiera deklaracje zmiennej

    -   drugi podfolder zawiera warunek logiczny

    -   trzeci podfolder zawiera instrukcję let - przypisania wartości
        do zmiennej

    -   czwarty podfolder zawiera kod wykonany w przypadku spełnienia
        warunku

Print
-----

Służy wypisaniu tekstu na ekran. Drugi katalog komendy musi zawierać
jeden podfolder przetrzmujący listę argumentów, które zostana wypisane
na ekran.

Invoke function
---------------

Wywołanie funkcji musi zawierać 2 podkatalogi. Pierwszy z nich zawiera
listę argumentów z jaką wywołujemy funkcję, drugi z nich jest linkiem do
deklaracji funkcji odwołującym się do stosu zewnętrznej funkcji lub
globalnej w przypadku niepowodzenia wyszukiwania w stosie funkcji matki.

## [Instrukcja](#instrukcja)

Przykładowe struktury programów
-------------------------------

Instrukcja Uruchomiania
-----------------------

Aby uruchomić przykładowy program należy uruchomić skrypt *main.py*.
Przykładowa komenda uruchamiająca interpreter wygląda: *python main.py
ścieżka\_do\_głównego\_katalogu\_programu* Udostępniono również tryb
debugowania, który pozwala na dokładną obserwację wydarzeń, które dzieją
się podczas interpretacji programu. Aby uruchomić interpretację w trybie
debugowania po nazwie skryptu(main.py) należy dopisać *-d*. Dodatkowo
istnieje możliwość zapisu logów do pliku, komenda uruchamiająca program
wygląda wtedy: *python main.py -df ścieżka\_docelowa\_pliku\_log
ścieżka\_do\_głównego\_katalogu\_programu*

### Kreator podstawowych zmiennych

Aby przyspieszyć żmudne tworzenie programów stworzono skrypt
automatyzujący tworzenie zmiennych typów:

-   int

-   float

-   boolean

-   char

-   string

Są one tworzone w formacie gotowym do deklaracji tj. katalog zawierający
3 podkatalogi które określają typ, wartość oraz nazwę zmiennej.
Funkcjonalność udostępniona jest w skrypcie
*/utilities/variable\_creator.py*. Korzystanie ze skryptu jest bardzo
proste przykładowa komenda: *python variable\_creator.py
sciezka\_w\_ktorej\_powstanie\_zmienna int 25 a* jest odpowiednikiem int
a=25.
