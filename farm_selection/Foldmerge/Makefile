#----------------------------------------------------------------------
# Przyklad linkowania bibliotek systemu ROOT z wlasnym programem
#----------------------------------------------------------------------
.SUFFIXES:  .o .c .cxx .cpp .C .f .l  .s  .sh  .h  .a
#======================================================================
# Biblioteki ROOTa dla linkera
# 1) Jawnie:
##  Sciezka to systemu ROOT - nalezy ja ustawic odpowiednio
#RPATH = /home/username/ROOT/

#RLIB=   -L$(ROOTSYS)lib -lCore -lHist -lGraf -lGraf3d -lGpad -lTree -lMathCore -lRooFitCore -lRooFit \
        -lRint -lRIO -lPostscript -lMatrix -lPhysics -lMinuit -lm -ldl -lpthread -rdynamic -Wl,--no-as-needed $(ROOTGLIBS)

#Root 6 config
RLIB=   -L$(ROOTSYS)  -lgsl -lpthread -lpcre -lNet -lRIO -lThread -lMinuit -lFoam -lGraf -lGpad -lHist -lMatrix -lCore -lMathCore -lMathMore -lTree -lRooFitCore -lRooFit

#Root 5 config
#RLIB=   -L$(ROOTSYS) -lCint -lgsl -lpcre -lNet -lRIO -lThread -lMinuit -lFoam -lGraf -lGpad -lHist -lMatrix -lpthread -lCore -lMathCore -lMathMore -lTree -lRooFitCore -lRooFit

# 2) Niejawnie, przy uzyciu root-config
#RLIB= `root-config --libs`
#======================================================================
# Nazwa biezacego katalogu
DIRNAME = ./
#======================================================================
# Nazwa rdzeniowa modulu programu
#NAME1 = RooMinuitMCMC
NAME2 = merge
#NAME2 = generatory
# Pliki objectowe (po kompilacji)
#OBJT1 = $(NAME1).o
OBJT2 = $(NAME2).o
# Pliki wykonawcze (po linkowaniu)
#EXEC1 = $(NAME1).x
EXEC1 = $(NAME2).x
# Nazwa i opcje kompilatora
CXX = g++ -std=c++11
# 1) Jawnie
#CXXFLAGS = -O -Wall -pthread -I$(RPATH)include
# 2) Przy uzyciu root-config
CXXFLAGS = -O2 -Wall `root-config --cflags`
# Nazwa i opcje linkera
LD = $(CXX)
LDFLAGS = `root-config --ldflags`
#==============================================================================
# Kompilacja dla modulow z plikami naglowkowymi
%.o: %.cxx %.h
	$(CXX) $(CXXFLAGS) -c $<
# Kompilacja dla modulow bez plikow naglowkowych
%.o: %.cxx
	$(CXX) $(CXXFLAGS) -c $<
#==============================================================================
.PHONY: all run clean tar
all: ${EXEC1}
#==============================================================================
# Linkowanie
${EXEC1}: ${OBJT1} ${OBJT2}
	$(LD) -o $@ $(LDFLAGS) $^ $(RLIB)
#==============================================================================
# Uruchamianie
run: ${EXEC1}
	./${EXEC1}
#==============================================================================
clean:
	(rm -f *.o *.a *~ *.exe *.x core lmap *.dvi *.aux *.log a.out)
#==============================================================================
tar: clean
	(cd ../; tar -cvzf $(DIRNAME).tar.gz $(DIRNAME) )
#==============================================================================
# Wszelkie akcje jakie należy podjąć aby program zaprezentował swoje działanie:
test: run
	@echo 'Test run finished'
#==============================================================================
