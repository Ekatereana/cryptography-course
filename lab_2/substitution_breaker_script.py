from generic_algo import GeneticAlgo
from shared_code import alphabet

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
         "VPETKTMEHVPETCMEHVPETT")
    ]

    # third line solving:

    solver = GeneticAlgo('../assets/tri_grams_fq.csv', alphabet)
    text = solver.solve(bytes(intro_tasks[0], "ascii"))
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