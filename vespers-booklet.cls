\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{vespers-booklet}

\LoadClass[statementpaper, 10pt, twoside]{memoir}

\RequirePackage[utf8]{inputenc}
\RequirePackage[bitstream-charter]{mathdesign}
\RequirePackage{titlesec}
\RequirePackage{paracol}
\RequirePackage{mdframed}
\RequirePackage{paracol}

\RequirePackage[ecclesiasticlatin.usej, english]{babel}
\babelprovide[hyphenrules=liturgicallatin]{ecclesiasticlatin}

\RequirePackage[autocompile]{gregoriotex}

% memoir page format setup
\settrims{0pt}{0pt}
\settypeblocksize{7in}{4.25in}{*}
\setlrmargins{*}{*}{1.4}
\setulmargins{*}{*}{1.2}
\setheadfoot{\onelineskip}{2\onelineskip}
\setheaderspaces{*}{.8\onelineskip}{*}

\checkandfixthelayout

\setlength{\parskip}{4pt plus 2pt minus 1pt}
\setlength{\parindent}{0pt}
\setlength{\stanzaskip}{4pt plus 2pt minus 1pt}

\pagestyle{plain}

\titleformat{\chapter}[block]{\huge\scshape\filcenter}{}{1em}{}
\titleformat{\section}[block]{\Large\bfseries\filcenter}{}{1em}{}

\setlength{\columnseprule}{0.4pt}

\mdfsetup{skipabove=\topskip, skipbelow=\topskip}

\newcommand{\rubric}[1]{
	\switchcolumn[0] {
		\selectlanguage{english}\itshape
		#1
	}
}

\newcommand{\latinenglish}[2]{
	\switchcolumn[0]* {
		\selectlanguage{ecclesiasticlatin}
		#1
	}
	\switchcolumn[1] {
		\itshape\small
		#2
	}
}

\newenvironment{latinenglishsection}
	{\columnratio{.5, .5} \begin{paracol}{2}}
	{\end{paracol}}

\newenvironment{versicles}{\par\leavevmode\parskip=0pt}{}

\newenvironment{collect}
{
	\leavevmode
	\parindent=1em
	\parskip=0pt
	\noindent Orémus.\par
}{}

\newenvironment{optionbox}
{
	\switchcolumn[0]
	\begin{mdframed}
%	\begin{minipage}{0.8\linewidth}
}{
%	\end{minipage}
	\end{mdframed}
}

\newcommand{\optionrule}{
	\begin{center}
	\rule{0.5\linewidth}{0.6pt}
	\end{center}
}

\newenvironment{optionruled}
{
	\optionrule
}
{
	\optionrule
}

% for use inside the collect environment
\newcommand{\Amen}{\par\noindent \Rbar. Amen.}