# **スプレッドシートによるオントロジーとスタイルシートの定義**

2025-04-20 橋田  
青字の部分は未実装。

1. # **共通定義**

## **特殊記号 : ; ( ) \[ \] ? \* \+ | ' \\**

(): グループ化  
\[\]: 囲まれた文字のうちのいずれか。「-」で文字の範囲を表わす。\[の直後^の場合、その後の文字以外の文字を表わす。  
A?: 1回以下のA  
A\*: 0回以上のA  
A+: 1回以上のA  
A|B: AまたはB

' 'で囲まれた記号は特殊な意味を持たない。  
\\で始まるセルはコメント(下記Cmt)。  
labelとabbrevの値に特殊記号を含めないこと。

## **文字と語**

UCAlpha ::= \[A-Z\]  
LCAlpha ::= \[a-z\]  
Alpha ::= \[UCAlpha LCAlpha\]  
Digit ::= \[0-9\]  
PInteger ::= \[1-9\] Digit\*  
Integer ::= '0' | '-'? PInteger  
Decimal ::= Integer ('.' Digit+)?  
AlphaNumeric ::= \[Alpha | Digit\]  
ID ::=  (Alpha | '\_') (AlphaNumeric | '.' | '-' | '\_')\*  
Cmt ::= ‘\\’ Character\*  
Comments ::= Cmt? BRComments  
BRComments ::= (BR+ Cmt)\*

Character: 文字  
SP: 1個以上の空白文字(スペース、タブ、改行)の列  
BR: セルの区切り  
NL: 改行

2. # **オントロジー**

Ontology ::= OntologyHeader BRComments  
(NL NameSpaceDefinition)\*  
(NL (Type (BR Type)\* BRComments | Comments))+

TypeのセルがN列にわたってスパンしていることがあるが、それは縦に並んだ同じ内容のN個のセルと見なす。

OntologyHeader ::= '\]O’ SP ID SP Label  
Type ::= Class | DataType | Property

## **ラベル**

Labels ::= Label ('|' Abbrev ('|' Comment ('|' Formats ('|' ImageURI)?)?)?)?  
Label \= Abbrev \= Comment ::= LocatedWord (';' LocatedWord)\*  
LocatedWord ::= (Locale ':')? Word  
Formats ::= LocatedFormat (';' LocatedFormat)\*  
LocatedFormat ::= (Locale ':')? Format  
Format ::= (EmbeddedFormat | Expression | Word)+  
EmbeddedFormat ::= ‘{‘ (Expression | Word)+ ‘}’  
Expression ::= ‘\[‘ (Function? Variable | ArithmeticExpression) ‘\]’  
Function ::=  ‘sum’ | ‘ave’ | ‘card’ |  ‘ini’ | ‘fin’ | ‘list’ | ‘date’ | ‘time’  
Variable ::= '\[' (‘&’ Alpha+ | ‘%’ NormalClassID)? (\[%\$\] PropertyID)\* '\]'  
ArithmeticExpression ::= ‘-‘ SubExpression | SubExpression \[+\\-\*/\] SubExpression  
SubExpression ::= Function? Variable | ‘(‘ ArithmeticExpression ‘)’

Label: ラベル(rdfs:label)  
Abbrev: ラベルの短縮表記(menu:abbrev)  
Comment: コメント(rdfs:comment)  
Format: 書式; \[%bloodPressureMax\]/\[%bloodPressureMin\]mmHgなど  
Locale: ISO 639-1の2文字の言語コード; ja、en、cn、kr、fr、deなど  
Word: 任意の文字列; 特殊記号(;:|\[\]{}\\)を含める場合は\\でエスケープ  
sum: 総和  
ave: 算術平均  
ini: 初期値  
fin: 最新値(省略可能)  
list: リスト(順序付き集合)  
date: 日時のうち日付  
time: 日時のうち時刻  
Variable: 変項  
&: subjectなど特定の変項  
%: クラスのインスタンスの属性;  
   たとえば\[%high\]はFormatを含むクラスのインスタンスのhigh属性の値  
\$: クラスそのものの属性  
\[\]はFormatを含む属性の値  
ImageURI: 画像のURI

ClassID ::= (Prefix ':')? (NormalClassID | ChoiceClassID)  
NormalClassID ::= UCAlpha (AlphaNumeric | '.' | '-' | '\_')\*  
ChoiceClassID ::= '\_' Alpha (AlphaNumeric | '.' | '-' | '\_')\*  
PropertyID ::= (Prefix ':')? LCAlpha (AlphaNumeric | '.' | '-' | '\_')\*

ClassID: クラスのID  
NormalClassID: 通常のクラスのID  
ChoiceClassID: 選択肢クラスのID  
PropertyID: 属性のID

### **例1:**

The United States of America|USA  
 ↓  
{ "label": "The United States of America",  
  "abbrev": "USA" }

### **例2:**

ja:血圧;blood pressure|BP||\[%bloodPressureMax\]/\[%bloodPressureMin\]mmHg  
↓  
{ "label": { "ja": "血圧", "": "blood pressure" },  
  "abbrev": "BP",  
  "format": "\[%bloodPressureMax\]/\[%bloodPressureMin\]mmHg" }

## **クラス**

クラスのIDは英大文字か’\_’で始まるとする(たとえば下の例1の’Human’)。左隣のセルで定義されたクラスを親クラス(rdfs:subPropertyOfの値)とする。

Class ::= (NormalClassID | ChoiceClassID ‘\!’?) (SP Labels)?

\!: 選択肢クラスがデフォルト値であることを示す(menu:selected)

### **例1:**

| Human ja:人間;Human | Male ja:男性;Male |
| :---- | :---- |
|  | Female ja:女性;Female |

  ↓  
{ "@id" : "\#Human",  
  "@type" : "Class",  
  "label": { "ja": "人間", "": "Human" }},  
{ "@id" : "\#Male",  
  "@type" : "Class",  
  "subClassOf" : "\#Human",  
  "label": { "ja": "男性", "": "Male" }},  
{ "@id" : "\#Female",  
  "@type" : "Class",  
  "subClassOf" : "\#Human",  
  "label": { "ja": "女性", "": "Female" }}

### **例2:**

| \_Selection | Value1 |
| :---- | :---- |
|  | Value2\! |

  ↓  
{ "@id" : "\#\_Selection", "@type" : "Class" },  
{ "@id" : "\#Value1", "@type" : "Class", "subClassOf" : "\#\_Selection" },  
{ "@id" : "\#Value2", "@type" : "Class", "subClassOf" : "\#\_Selection",  
  "selected": true }

選択肢クラスは名前を\_から始め、サブクラスも選択肢とする。上の例の場合、\_Selectionを値域に持つ属性の値はAかBであり、デフォルト値はBとなる。

## **属性**

属性のIDは英小文字で始まるとする。左隣のセルで定義されたクラスを定義域(rdfs:domainの値)またはその下位クラスととする。つまり、各属性の始点の型は、オントロジーの定義において左隣に現われたクラスのいずれか。  
左隣のセルで定義された属性を親属性(rdfs:subPropertyOfの値)とする。  
右隣のセルで定義されたクラス(データタイプを含む)を値域(rdfs:rangeの値)またはその下位クラスとする。つまり、各属性の終点の型は、オントロジーの定義において右隣に現われるクラスのいずれか。  
Property ::= PropertyID (‘ @’ NormalClassID)\*  ‘/’?  
('\*' | '=' PInteger | (')' PInteger)? ('(' PInteger)?)? (SP Labels)?

@: NormalClassID (FunctionalProperty、SymmetricPropertyなど)が属性の型  
/: 入力インタフェースを表示しない(menu:invisible)  
\*: 定義域クラスのowl:Restrictionに出現させない  
\=: この属性はちょうどPInteger個ある(owl:cardinality)  
(: この属性は高々PInteger個ある(owl:maxCardinality)  
): この属性はPInteger個以上ある(owl:minCardinality)

表示・入力すべき属性はクラスの限定owl:Restrictionから得る。したがって、\*によりクラスの限定に出現させないことで、UIに現れない属性となる。

## **データタイプ**

DataType ::= DataTypeID ('/' Period)? ('\!' Word)?  
((\[)\>\] Decimal)? (\[(\<\] Decimal)? | ('+' Word)? ('-' Word)?)

DataTypeID: データタイプ名; string、integer、positiveInteger、boolean、date、dateTimeなど  
/: Periodが時間の粒度(DataTypeIDはdateかdateTime)。  
\!: Wordがデフォルト値。  
): 属性値がDecimal以上であるまたはDecimal以上の長さである(minInclusive、minLength)  
\>: 属性値がDecimalより大きい(menu:minExclusive)  
(: 属性値がDecimal以下であるまたはDecimal以下の長さである(maxInclusive、maxLength)  
\<: 属性値がDecimalより小さい(menu:maxExclusive)  
\+: Wordは属性値が真偽の場合に真を表わす文字列(menu:trueSymbol)  
\-: Wordは属性値が真偽の場合に偽を表わす文字列(menu:falseSymbol)

### **例1:**

| Try 試行 | okng\* 結果 | boolean\!false+OK-NG |
| :---- | :---- | :---- |
|  |  | result1=1 結果1 |
|  |  | result2(1 結果2 |

  ↓  
{ "@id" : "\#Try",  
  "@type" : "Class",  
  "label" : "試行"  
  "subClassOf" : \[  
  { "@type" : "Restriction",  
    "onProperty" : "\#result1",  
    "cardinality" : 1 },  
  { "@type" : "Restriction",  
    "onProperty" : "\#result2",  
    "maxCardinality" : 1 } \] },  
{ "@id" : "\#okng",  
  "@type" : "DatatypeProperty",  
  "domain" : "\#Try",  
  "range" : "boolean",  
  "label" : "結果",  
  "trueSymbol" : "OK",  
  "falseSymbol" : "NG",  
  "defaultValue" : false },  
{ "@id" : "\#result1",  
  "@type" : "DatatypeProperty",  
  "subPropertyOf" : "\#okng"  
  "label" : "結果1" },  
{ "@id" : "\#result2",  
  "@type" : "DatatypeProperty",  
  "subPropertyOf" : "\#okng"  
  "label" : "結果2" }

### **例2:**

| sex | \_Male |
| :---- | :---- |
|  | \_Female |
|  | \_Unknown |

 ↓  
{ "@id" : "\#sex",  
  "@type" : "ObjectProperty",  
  "range" : "\#\_X8uE0v" },  
{ "@id" : "\#\_X8uE0v",  
  "@type": "Class" },  
{ "@id" : “\#\_Male”,  
  “@type”: “Class”,  
  "subClassOf" : "\#\_X8uE0v" },  
{ "@id" : “\#\_Female”,  
  “@type”: “Class”,  
  "subClassOf" : "\#\_X8uE0v" },  
{ "@id" : “\#\_Unknown”,  
  “@type”: “Class”,  
  "subClassOf" : "\#\_X8uE0v" }

\_X8uE0vは自動生成する。自動生成されたクラスは入力メニューに表示しない。

### **例3:**

| X | a |
| :---- | :---- |
| Y | a |

 ↓  
{ “@id”: “\#X”,  
  “@type”: “Class”,  
  “subClassOf”: “\#\_Ni91U3o” },  
{ “@id”: “\#Y”,  
  “@type”: “Class”,  
  “subClassOf”: “\#\_Ni91U3o” },  
{ “@id”: “\#\_Ni91U3o”,  
  “@type”: “Class” },  
{ “@id”: “\#a”,  
  “@type”: “ObjectProperty”,  
  “domain”: “\#\_Ni91U3o” }

### **例4:**

| point 点数|||\[\]点 | positiveInteger\!50)0(100  |
| :---- | :---- |

  ↓  
{ "@id" : "\#point",  
  "@type" : "DatatypeProperty",  
  "range" : "positiveInteger",  
  "label" : "点数",  
  "format": "\[\]点",  
  "minInclusive" : 0,  
  "maxInclusive" : 100,  
  "defaultValue" : 50 }

## **アプリのUIでの表示**

以下において”ABBREV”は”abbrev (なければlabel)”を意味する。  
abbrevかlabelを表示すべきときにいずれの値もなければ何も表示しない。  
テキストの表示において連続する複数のスペースは1つのスペースに縮約する。

\[boolean以外のリテラルの表示\] 

* 日時(dateやdateTime)は所定の書式で  
  日本語ロケールなら”2024年6月22日23:30”など  
* 10進数(decimal)は所定の精度で  
* 他(整数やanyURIやstring)はそのまま

\[formatの表示\] formatを表示するとは、その値の表示において”\[…\]”の代わりに対応する属性値を次のように表示することである。

* エンティティ(非選択肢クラスのインスタンス)は下の\[エンティティの表示\]  
* 選択肢は属性のabbrevに続けて選択肢クラスのABBREV  
* mmdataはタイトルとコメントと添付ファイル  
* booleanは、真偽のABBREVがあれば属性のabbrevに続けて真偽のABBREV、真偽のABBREVがなければ真のときだけ属性のABBREV  
* 他は上の\[boolean以外のリテラルの表示\]

\[属性値フィールド内の表示\] エンティティダイアログにおいて各属性値フィールド内を値の種類に応じて以下のように表示する。

* エンティティは下の\[エンティティの表示\]  
* mmdataはタイトルとコメントと添付ファイル  
* 選択肢は選択肢クラスのlabel  
* booleanは、真偽のlabelがあればlabel、なければ真のときだけ”✔”  
* 他は、属性のformatがあればformat (**属性値フィールドの表示で直接formatを使うのはここだけ**)、なければ上の\[boolean以外のリテラルの表示\]

\[エンティティの表示\] タイムラインに表示するエンティティ(アイテム)およびエンティティダイアログの属性値フィールドに表示するエンティティについては、

1. エンティティダイアログの属性値フィールドに表示するエンティティの場合は事象ならbeginとendを表示  
2. クラスのlabelを太字で表示  
   ただし、エンティティが属性値であってそのクラスが1つに限られる場合はクラスのlabelを表示しない  
3. クラスのformatを表示  
   クラスのformatの中の”{…}”はその中のVariableの値がすべて存在するときに有効とする。たとえば、formatの値が”{\[%start\]から\[%goal\]まで}”のとき、start属性とgoal属性の値が各々”東京”と”大阪”ならば”東京から大阪まで”と表示するが、start属性かgoal属性が値を持たなければ何も表示しない。  
   複数の値を持つ属性がある場合はformatの展開が複数通り?  
4. クラスのformatに含まれない属性を以下の要領で表示  
- 値がエンティティなら、属性がformatを持てば属性のabbrevに続けてformat  
- 値が選択肢なら、属性のabbrevに続けて、選択された選択肢のクラスのABBREV  
- 値がbooleanなら、属性がformatを持てばformat、持たなければ真のときだけ属性のABBREV  
- 値が数(integerやdecimal)か日時(dateやdateTime)なら、属性がformatを持てばformat、持たなければ属性のabbrevに続けて\[boolean以外のリテラルの表示\]  
- 他のリテラル(string、anyURIなど)は、属性がformatを持てば属性のabbrevに続けてformat  
- タイムラインのアイテムのトップレベルのcnt属性はアイテムの下部に所定の背景色で表示  
- 他のmmdata値の属性は、formatを持てばformat、持たなければタイトルとコメントと添付ファイル  
  1つの属性の値が複数個ある場合でも属性のABBREVは高々1回だけ表示

たとえば下記の属性定義に対して”数学68点”のように表示する。

| math 数学の成績|数学||\[\]点 | positiveInteger |
| :---- | :---- |

3. # **オントロジーの限定**

下位クラスのないクラスと選択肢クラスはデフォルトで入力可能(入力メニューから選択可能)。それ以外のクラスはデフォルトで入力不可能。  
自動生成されたものを除くあらゆるクラスがデフォルトで入力メニューに表示される。  
最上位のクラスとその直下のクラスはデフォルトでメニューの根になる。

Restriction ::= RestrictionHeader BRCommentts  
(NL NameSpaceDefinition)\*  
(NL (Restriction (BR Restriction)\* BRComments | Comments))+  
RestrictionHeader ::= '\\R’ SP ID SP Label?  
Restriction ::= (ClassID | PropertyID) SP InputRestriction? OutputRestriction?  
InputRestriction ::= \[RhHXiIeEbB\]  
OutputRestriction ::= \[yYnN\]

R: メニューの根になる(入力は不可)  
h: メニューにグレーで表示し選択(入力)不可とする  
H: メニューに表示せず、下位クラス/属性はiとIの場合のみメニューに表示する  
~~x: メニューに表示しない~~  
~~X: メニューに表示せず、メニュー生成処理を以下に進めない(ゆえに下位クラス/属性はiとIの場合もメニューに表示されない)~~  
i: 入力可  
I: 入力可であり、下位クラス/属性はR、h、H、Xの場合のみ入力不可  
e: 他者が作ったデータでも編集可  
E: 他者が作ったデータでも編集可であり、下位クラス/属性も編集可  
y: 出力可  
Y: 出力可であり、下位クラス/属性はnとNの場合のみ出力不可  
n: 出力不可  
N: 出力不可であり、下位クラス/属性はyとYの場合と自分が記録者である場合のみ出力可  
m: 他者が追加可能  
M: 他者が追加可能であり、下位属性はR、h、H、Xの場合のみ追加不可  
t: タイムラインとグラフに表示しない  
T: 下位クラスもタイムラインとグラフに表示しない

Restrictionのセルが1行に複数個あっても良い

4. # **制約**

Constraint ::= ConstraintHeader BRComments NL  
ConstraintArgument (BR ConstraintArgument)\* BRComments  
(NL (Conditions? BRComments | Comments))+  
ConstraintHeader ::= '\\C’ SP ID SP Label? BR EventVariable (SP EventVariable)\*  
EventVariable ::= NormalClassID (‘:’ Period)?  
ConstraintArgument ::= ‘make’ CArgument | CFunction? CArgument  
| ArithmeticConstraintExpression  
CArgument ::= ‘\[‘ Pinteger? (‘%’ PropertyID)\* (‘%’ ClassID)? ‘\]’  
Conditions ::= Condition (BR Condition)\*  
Condition ::= Comparison (SP Comparison)\* | ClassID | ‘true’ | ‘false’  
Comparison ::= (\[)\>(\<^\]? (Decimal | Period)) | (\[\~)\>(\<^\] ConstraintExpression)  
Period ::= Pinteger? \[yMwdHms\]  
ConstraintExpression ::= CFunction? CArgument  
| ArithmeticConstraintExpression  
CFunction ::=  ‘sum’ | ‘ave’ | ‘card’ | ‘ini’ | ‘fin’  
ArithmeticConstraintExpression ::= ‘-‘ SubConstraintExpression  
| SubConstraintExpression \[+\\-\*/\] SubConstraintExpression  
SubConstraintExpression ::= ConstraintExpression  
| ‘(‘ ArithmeticConstraintExpression ‘)’

ConstraintExpressionにJavaScriptの関数呼び出しを加える?

EventVariable: 事象を表わす変項  
CArgument: Pinteger番目の変項から0個以上のPropertyを辿った先の値  
card: 個数  
make: 属性の作成  
Period: 連続した整数個の時間単位; たとえば2dは現在時刻を含む日の前日の0:00から48時間; 主変項、主変項を含む問診が含む事象、および稀少事象(rare event; 誕生や妊娠や既往歴や問診)においては省略  
y: 年(1月1日～12月31日)  
M: 月(1日～晦日)  
w: 週(日曜日の0:00から次の日曜日の0:00)  
d: 日(0:00から24時間)  
H: 時間(X時0分から60分間)  
m: 分(X時Y分0秒から60秒間)  
s: 秒(X時Y分Z璒から1秒間)  
Condition: 対応する(同じ列の) ConstraintArgumentが満たすべき条件。  
\~: ConstraintArgument \= ConstraintExpression  
): ConstraintArgument ≧ ConstraintExpression  
\>: ConstraintArgument \> ConstraintExpression  
(: ConstraintArgument ≦ ConstraintExpression  
\<: ConstraintArgument \< ConstraintExpression  
^: ConstraintArgument ≠ ConstraintExpression

ConstraintHeaderの’\]C’の次のIDはオントロジーのIDと異なる必要がある。

ConstraintHeaderの第2のセルの中の最初のEventVariableを**主変項**、他のEventVariableを**副変項**と呼ぶ。副変項の開始日時(begin)は主変項の開始日時より前であり、副変項のPeriodの最後の単位時間(5dなら最終日)は主変項の開始日時を含む。EventVariableに対応するノードを入力・編集しようとするときは、それを主変項として含む制約を適用する。その際、**副変項に対応するノードは作成および手動編集はするが自動編集・削除はしない**。また、制約処理中は手動の編集を禁止する。主変項の手動による編集の際に副変項を手動で編集できないようにする。

ConstraintExpressionにおいてCFunctionがない場合のデフォルトはfinとする。たとえば\[1%a\]は第1副変項のa属性の最後の値。

制約が満たされるとは、ある条件行(Conditions)が満たされることであり、条件行が満たされるとはそのすべての条件(Condition)が満たされることである。条件が満たされるとは、同じ列にある制約の項(ConstraintArgument)の値がその条件を満たすか、その制約の項がmake\[CArgument\]の形であって条件が自然数(の範囲)を指定することである。満たされた条件行が複数あっても良い。

CArgumentの形のConstraintArgument Xが～CArgumentの形の条件Yを満たすには、Xの(0個以上の)値をYの(0個以上の)値と1対1に対応させ、対応する値を共有する。たとえば下記の制約では、X%a%bの値をY%c%dの値と1対1に対応させる。a属性とb属性の個数はX%a%bとY%c%dの個数が等しくなるように決める(たとえば”a=1”で”b)1”なら唯一に決まる)。

| \]C XY XY | X Y |
| ----- | ----- |
| \[%a%b\] |  |
| \~\[1%c%d\] |  |

ConstraintArgument (制約の項)のうち’make’ CArgumentの形のものは、有効な条件が1以上の値のときその値の個数だけ中のCArgumentを生成する。

ConstraintArgumentの値Vを**外部設定**(手入力か他の制約によって値を設定)できるのは、そのConstraintArgumentがCArgumentの形であり、ある条件行において、対応する条件をVが満たすことが即座にわかり(それには条件の中の変項の値がすべて決まっている必要がある)、他のConstraintArgumentのうち値を更新するものが対応する各条件を満たすような値の可能な組合せが1個以上で有限個の場合である。ただし、外部設定によって他の制約を満たさない場合はその外部設定ができないとする。

たとえば下記の制約では、\[%a\]の値を外部設定すると\[%b\]の値が一意に決まるが、\[%b\]の値を外部設定によって更新しようとすると\[%a\]の可能な値が無限個になるので\[%b\]の外部設定はできない。

| \]C ab ab | Y |
| ----- | ----- |
| \[%a\] | \[%b\] |
| \<3 | \~\_Small |
| )3 \<9 | \~\_Normal |
| )9 | \~\_Large |

下記の制約では、\[%a\]が\_YES、\[1%b%c\]が\_White、\[%p\]が2のとき、外部設定により\[%a\]を\_NOにすると\[1%b%c\]が\_Redになり、\[%p\]は変わらない。\[%a\]が\_YES、\[1%b%c\]が\_White、\[2%p\]が0のときは、\[%a\]を\_NOに更新すると\[2%p\]の取り得る値が無限にあるので、外部設定で\[%a\]を\_NOすることはできず、同じく\[1%b%c\]を\_Redにすることもできない。\[%a\]が\_YES、\[1%b%c\]が\_Red、\[%p\]が0.5のとき、外部設定により\[1%b%c\]を\_Whiteに更新することができ、このとき\[2%p\]は変わらない。

| \]C XYZ XYZの関係 | Z X:4d Y:2d |  |
| ----- | ----- | ----- |
| \[%a\] | \[1%b%c\] | \[2%p\] |
| \~\_YES | \~\_White |  |
| \~\_YES | \~\_Red | \>0 \<1 |
| \~\_NO | \~\_Red | )1 |

制約Cが属性Pを含むとは、PがCの項(ConstraintArgument)であるか、Cのある条件(Condition)がPを含むこと。複数の制約が依存するとは、それらが共通の属性を含むこと。依存する制約は同時に処理される。  
人手編集などの外部入力によってある属性の値を更新しようとしたとき、その属性を含む制約およびその制約と項を共有関係で直接間接につながった制約の処理が起動される。それらの制約の拡張条件行(各制約から条件行を1つずつ選んだ組合せ)のうち外部入力と整合するものを見付けるのが制約処理である。

5. # **タイムラインのスタイルシート**

タイムライン画面では入出力可能。

TimeLine ::= TimeLineHeader BRComments  
(NL (TimeLineElement (BR TimeLineElement)\* BRComments  
| Comments))+  
TimelineHeader ::= '\\T’ SP ID SP \[SR\] SP Label  
TimelineElement ::= \[YN\] SP TimelinePath SP Condition?  
TimelinePath ::= ‘|’? NormalClassID (‘%’ PropertyID)\*  
| NormalClassID? (‘%’ PropertyID)\* ‘|’ (‘%’ PropertyID)+

S: 1人の記録対象者のデータのタイムライン  
R: 1人の記録者のデータのタイムライン  
|: 出力可・不可の範囲の開始  
Y: 下位クラス等も出力可  
N: 下位クラス等も出力不可

6. # **グループサマリのスタイルシート**

グループサマリ画面では入出力可能。

GroupSummary ::= GroupSummaryHeader BRComments  
(NL (GroupSummaryElement BRComments | Comments))+  
GroupSummaryHeader ::= ’\]G’ SP ID SP (‘S’ | ‘R’ | ‘\[‘ NormalClassID ‘\]’)  
SP Period SP Label  
GroupSummaryElement ::= Event SP Function SP? Format  
Event ::= (NormalClassID | NormalClassID? (‘%’ PropertyID)+)

S: グループサマリの各行が1人の記録対象者  
R: グループサマリの各行が1人の記録者  
NormalClassID: グループサマリの各行がその型の1個の事象  
Period: 表示範囲の期間  
GroupSummaryElement: グループサマリの1列; 最初(ini)または最後(fin)またはすべて(list)のEventをFormatに従って表示

7. # **チャネルサマリのスタイルシート**

チャネルサマリ画面では各Variableの入力・編集が可能。

ChannelSummary ::= '\]S’ SP ID SP Label SP Period BRComments  
(NL (BR\* Element (BR+ Element)\* BRComments  
| Comments))+

Element ::= Style ‘|’ Formats (‘|’ Scope)\*  
Style ::= (Table | Graph) Width? (SP Color)?

コメントのみを含む行を無視した場合に上下に隣接する2つのセルのElementに対応する表示(表のセルまたはグラフのデータポイント)は横方向のサイズも位置も同じでなければならない。コメントも含まない完全な空行は、その上下の表やグラフが別のものであり、同じ列のセルの横方向の位置が異なっても良いことを意味する。

Table ::= \[nb\] \[LRTB\]?

n: 表の枠線なしセル  
b: 表の枠線付きセル  
L: 左寄せ  
R: 右寄せ  
T: 上寄せ  
B: 下寄せ  
中寄せがデフォルト。

Graph ::= \[LBG\]

L: 折れ線グラフの縦軸  
B: 棒グラフの縦軸  
G: グラフのデータ

Width ::= Decimal ‘em’?

表の各セル(グラフの各データポイントの領域)の幅。1行のうちemで指定されたセルの幅を画面の幅から除いた幅を他の各セルのDecimalの値(デフォルトは1)で比例配分したものが各セルの幅。

Color: グラフの線と文字または表の文字の色

Scope ::= \[HV\]? Variable? (TemporalRange | NumericRange | OntologicalRange)

H: 右向き繰返し  
V: 下向き繰返し

TemporalRange ::= Period Period?

たとえば4wは現在を含む週(日～土)で終わる4週間、3d2hは現在を含む日で終わる3日間の2時間単位への分割(36回の繰返し)。ScopeにTemporalRangeがあればVariableの属性のデフォルトはbegin。たとえば3d2hというScopeは、現在を含む日で終わる3日間を2時間単位に分割した場合の各単位内にbeginの値があるような事象の36個の集合を指定する。

NumericRange ::= ‘\[‘ Decimal SP Decimal (SP Decimal)? ‘\]’  
最初のDecimalは初期値、2番目は終値、3番目は増分。たとえば\[0 10 3\]は\[0, 3, 6, 9\]という数列を表わす。\[2 5\]は、Variableの値域がintegerの場合は\[2, 3, 4, 5\]という数列、decimalの場合は\[2, 5\]という区間を表わす。

OntologicalRange ::= ‘\[‘ ClassID (SP ClassID)\* ‘\]’  
1個以上のクラス(選択肢クラスでも良い)の和集合の範囲。

Scopeが指定する範囲はVariableの最初のクラスのインスタンスの集合であり、Variableの値の範囲はXXXRangeで指定される。たとえば、H\[%DrinkEat%foodMode\]\[\_mincedFood \_softFood\]というScopeが指定する範囲は、foodMode属性の値がmincedFoodかsoftFoodであるようなDrinkEatクラスのインスタンスの集合である。

Formatsの中のVariableの左端のクラスのインスタンスはScopeが指定する範囲に含まれる。たとえば、b|\[%Meal\$label\]|H\[%DrinkEat%foodMode\]\[\_mincedFood \_softFood\]というElementは、上記のScopeが指定する範囲内のDrinkEatクラスのインスタンスのうちMealクラスのインスタンスであるようなものの型であるクラスのlabel属性の値をそれぞれ枠線付きセルに入れて横に並べることを意味する。

左のScopeは右のScopeより広い。たとえばH\[%C%a\]\[1 3\]|V\[%D%b\]\[0 6 2\]は、H\[%C%a\]\[1 3\] (a属性の値域が整数とすると、その値が1、2、3であるCクラスのインスタンスの横方向の繰返し)の各回におけるV\[%D%b\]\[0 6 2\] (b属性の値が0、2、4、6であるDクラスのインスタンスの縦方向の繰返し)を表わす。またV2wd|V3d2hは、V2wd(現在を含む日を最終日とする2週間にわたる1日×14回の下向きの繰返し)の各回におけるV3d2h(その回の日における2時間×12回の下向きの繰返し)を表わす。ここで後者の3dのうち前者の各回に納まらない2日分は除外される。

あるセルCがHで始まるScopeを持たず、その直上(上隣とは限らない)のセルがHで始まるScopeを持てば、そのようなセルのうちCに最も近いもののHで始まるScopeがCに継承される。同じく、あるセルCがVで始まるScopeを持たず、その直左(左隣とは限らない)のセルがVで始まるScopeを持てば、そのようなセルのうちCに最も近いもののVで始まるScopeがCに継承される。継承されたScopeはCが持つScopeより広い。

Hで始まるScopeがあれば、それを含むセルに対応する表またはグラフの行のすぐ上にそのScopeを示すタイトル行を表示する。同じく、Vで始まるScopeがあれば、それを含むセルに対応する表またはグラフの列のすぐ左にそのScopeを示すタイトル列を表示する。

8. # **詳細ダイアログ(エンティティダイアログ)のスタイルシート**

各クラスについてそのインスタンスであるノードの詳細ダイアログのスタイルを指定する。内容はチャネルサマリとほぼ同じ。

EntityDialog ::= '\\E’ SP ID SP Label NormalClassID BRComments  
(NL (BR+ Element (BR+ Element)\* BRComments | Comments))+

Elementの中のVariableの左端はデフォルトでヘッダのNormalClassIDが指定するクラス。

9. # **名前空間**

オントロジー等において名前空間を定義する。

NameSpaceDefinition ::= ‘\]N’ SP Prefix SP User ‘\#’ Ontology  
Prefix ::= (ID | ‘\_’)  
User ::= ????  
Ontology ::= ID

Prefix: 名前空間の接頭辞  
User: PLR ID  
Ontology: オントロジーのID

名前空間の定義を含むオントロジー等においては、Userが所有するOntologyの中のクラスまたは属性XをPrefix:Xと書く。ただしPrefixが\_のときは:Xと書く。

以上  
