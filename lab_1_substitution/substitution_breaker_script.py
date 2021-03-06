from lab_1_substitution.generic_algo import GeneticAlgo
from lab_1_substitution.config import GeneticConf
from shared_code import alphabet
from lab_1_substitution.utils import calculate_n_grams, get_nth_letter
from lab_1_substitution.kasiski_examinator import calc_kasiski_factor
from lab_1_substitution.frequency_analisis import decrypt_text

TRIGRAM_SOURCE = '../assets/tri_grams_fq.csv'


def solve_third_paragraph(text: str):
    # third line solving:

    solver = GeneticAlgo(TRIGRAM_SOURCE, alphabet, GeneticConf(), 1)
    text = solver.solve(bytes(text, "ascii"))
    print(text)

    # result
    # ADDTHEAMIBITYTODELICHERANYKINDOPCOBYABCHAMETILSUMSTITUTIONLICHERS
    # THE ONE USED IN THE LICHER TEXTS HERE HAS TWENTY SIX INDECENDENTRANDOVBYLH
    # OSENVONOABCHAMETILSUMSTITUTIONCATTERNSPOREALHBETTERPROVENGBISHAB
    # CHAMETITISLBEARTHATYOULANNOBONGERREBYONTHESAVESIVCBEROUTINEOPGUE
    # SSINGTHEKEYMYEXHAUSTIFESEARLHWHILHYOUCROMAMBYUSEDTODELICHERTHECR
    # EFIOUSCARAGRACHWIBBTHEINDEXOPLOINLIDENLESTIBBWORKASASUGGESTIONYO
    # ULANTRYTODIFIDETHEVESSAGEINCARTSMYTHENUVMEROPLHARALTERSINAKEYAND
    # ACCBYPREQUENLYANABYSISTOEALHOPTHEVLANYOUPINDAWAYTOUSEHIGHERORDER
    # PREQUENLYSTATISTILSWITHTHISTYCEOPLICHERTHENEXTVAGILABWORDWIBBTAK
    # ETOTHENEXTBAMENJOYMITBYSBASHTWOLACITABYLACITABJLACITABMBLACITABY
    # LACITABB

    # Some letters still missplaced. Solve this.
    # (M - B, B - L)
    # (L - C , C - P, P - F)
    # (V - M, F - V)

    decipher = (
        " ADD THE AbIlITY DEcIpHER ANY KIND Of pOlYAlpHAbETIc"
        " SUbSTITUTION"
        " cIpHERS THE ONE USED IN THE cIpHER TEXTS HERE HAS "
        "TWENTY SIX INDEpENDENT RANDOVlY cHOSEN"
        " VONOAlpHAbETIc SUbSTITUTION pATTERNS"
        " fOR EAcH lETTER fROV ENGlISH AlpHAbET IT IS clEAR THAT YOU "
        " cAN NO lONGER RElY ON THE SAVE SIVplE ROUTINE Of GUESSING THE KEY "
        " bY EXHAUSTIFE SEARcH WHIcH YOU pRObAblY USED TO DEcIpHER"
        " THE pREFIOUS pARAGRApH WIll THE INDEX Of cOINcIDENcE STIll WORK"
        " AS A SUGGESTION YOU cAN TRY TO DIFIDE THE VESSAGE IN pARTS bY "
        " THE NUVbER Of cHARAcTERS IN A KEY AND ApplY fREQUENcY ANAlYSIS "
        " TO EAcH Of THEV cAN YOU fIND AWAY TO USE HIGHER ORDER fREQUENcY "
        " STATISTIcS WITH THIS TYpE Of cIpHER THE NEXT VAGIcAl WORD WIll TAKE "
        " TO THE NEXT lAbEN JOYbITlY SlASH TWO cApITAlY cApITAlJ cApITAl bl cApITAl YcAp IT All"
    )

    print(decipher
          .replace("M", "b")
          .replace("B", "l")
          .replace("L", "c")
          .replace("C", "p")
          .replace("P", "f")
          .replace("V", "m")
          .replace("F", "v"))


def solve_forth_paragraph(text: str):
    n_grams_pos = calculate_n_grams(text, 3, True)
    key_length = calc_kasiski_factor(n_grams_pos)
    solver = GeneticAlgo(TRIGRAM_SOURCE, alphabet, GeneticConf(True), key_length)
    text = solver.solve(bytes(text, "ascii"))
    print(text)


if __name__ == '__main__':
    intro_tasks = [
        ("EFFPQLEKVTVPCPYFLMVHQLUEWCNVWFYGHYTCETHQEKLPVMSAKSPVPAPV"
         "YWMVHQLUSPQLYWLASLFVWPQLMVHQLUPLRPSQLULQESPBLWPCSVRVWFLHL"
         "WFLWPUEWFYOTCMQYSLWOYWYETHQEKLPVMSAKSPVPAPVYWHEPPLUWSGYUL"
         "EMQTLPPLUGUYOLWDTVSQETHQEKLPVPVSMTLEUPQEPCYAMEWWYTYWDLUUL"
         "TCYWPQLSEOLSVOHTLUYAPVWLYGDALSSVWDPQLNLCKCLRQEASPVILSLEUM"
         "QBQVMQCYAHUYKEKTCASLFPYFLMVHQLUPQLHULIVYASHEUEDUEHQBVTTPQ"
         "LVWFLRYGMYVWMVFLWMLSPVTTBYUNESESADDLSPVYWCYAMEWPUCPYFVIVF"
         "LPQLOLSSEDLVWHEUPSKCPQLWAOKLUYGMQEUEMPLUSVWENLCEWFEHHTCGU"
         "LXALWMCEWETCSVSPYLEMQYGPQLOMEWCYAGVWFEBECPYASLQVDQLUYUFLU"
         "GULXALWMCSPEPVSPVMSBVPQPQVSPCHLYGMVHQLUPQLWLRPOEDVMETBYUF"
         "BVTTPENLPYPQLWLRPTEKLWZYCKVPTCSTESQPBYMEHVPETCMEHVPETZMEH"
         "VPETKTMEHVPETCMEHVPETT"),

        ("UMUPLYRXOYRCKTYYPDYZTOUYDZHYJYUNTOMYTOLTKAOHOKZCMKAVZDYBRO"
         "RPTHQLSERUOERMKZGQJOIDJUDNDZATUVOTTLMQBOWNMERQTDTUFKZCMTAZ"
         "MEOJJJOXMERKJHACMTAZATIZOEPPJKIJJNOCFEPLFBUNQHHPPKYYKQAZKT"
         "OTIKZNXPGQZQAZKTOTIZYNIUISZIAELMKSJOYUYYTHNEIEOESULOXLUEYG"
         "BEUGJLHAJTGGOEOSMJHNFJALFBOHOKAGPTIHKNMKTOUUUMUQUDATUEIRBK"
         "YUQTWKJKZNLDRZBLTJJJIDJYSULJARKHKUKBISBLTOJRATIOITHYULFBIT"
         "OVHRZIAXFDRNIORLZEYUUJGEBEYLNMYCZDITKUXSJEJCFEUGJJOTQEZNOR"
         "PNUDPNQIAYPEDYPDYTJAIGJYUZBLTJJYYNTMSEJYFNKHOTJARNLHHRXDUP"
         "ZIALZEDUYAOSBBITKKYLXKZNQEYKKZTOKHWCOLKURTXSKKAGZEPLSYHTMK"
         "RKJIIQZDTNHDYXMEIRMROGJYUMHMDNZIOTQEKURTXSKKAGZEPLSYHTMKRK"
         "JIIQZDTNROAUYLOTIMDQJYQXZDPUMYMYPYRQNYFNUYUJJEBEOMDNIYUOHY"
         "YYJHAOQDRKKZRRJEPCFNRKJUHSJOIRQYDZBKZURKDNNEOYBTKYPEJCMKOA"
         "JORKTKJLFIOQHYPNBTAVZEUOBTKKBOWSBKOSKZUOZIHQSLIJJMSURHYZJJ"
         "ZUKOAYKNIYKKZNHMITBTRKBOPNUYPNTTPOKKZNKKZNLKZCFNYTKKQNUYGQ"
         "JKZNXYDNJYYMEZRJJJOXMERKJVOSJIOSIQAGTZYNZIOYSMOHQDTHMEDWJK"
         "IULNOTBCALFBJNTOGSJKZNEEYYKUIXLEUNLNHNMYUOMWHHOOQNUYGQJKZL"
         "ZJZLOLATSEHQKTAYPYRZJYDNQDTHBTKYKYFGJRRUFEWNTHAXFAHHODUPZM"
         "XUMKXUFEOTIMUNQIHGPAACFKATIKIZBTOTIKZNKKZNLORUKMLLFBUUQKZN"
         "LEOHIEOHEDRHXOTLMIRKLEAHUYXCZYTGUYXCZYTIUYXCZYTCVJOEBKOHE")
    ]

    # solve_third_paragraph(intro_tasks[0])
    solve_forth_paragraph(intro_tasks[1])
