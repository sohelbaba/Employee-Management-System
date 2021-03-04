def leaveApprovedmessage(username, startdate, enddate):
    return '''
    Hello ''' + username + ''',
        
    We are happy to grant you leave request starting from ''' + startdate.split('T')[0] + '''  to  ''' + enddate.split('T')[0] + '''. We request you to complete all your pending work or any other important issue so that the company does not face any loss or problem during your absence. We appreciate your thoughtfulness to inform us well in advance.

    If you have any queries, please feel free to contact the Human Resources  Department. We look forward to your success in the company\n

    Thanks & Regards,
    Name of hr
    HR Executive 
    Direct: +91 6353235503 | W: www.lanetteam.com 
    406, Luxuria Business Hub, Nr. VR Mall, Surat, Gujarat - 395007. Ground Floor, I.T.P.I Building, Beside Celebration Mall, Bhuwana, Udaipur, Rajasthan - 313001'''


def leaveCanclemessage(username, startdate, enddate):
    return '''
    Hello ''' + username + ''',
        
    After reviewing your request, I am sorry to say that I am unable to grant your leave from ''' + startdate.split('T')[0] + '''  to  ''' + enddate.split('T')[0] + ''' . We appreciate your thoughtfulness to inform us well in advance.

    If you have any queries, please feel free to contact the Human Resources  Department. We look forward to your success in the company\n

    Thanks & Regards,
    Name of hr
    HR Executive 
    Direct: +91 6353235503 | W: www.lanetteam.com 
    406, Luxuria Business Hub, Nr. VR Mall, Surat, Gujarat - 395007. Ground Floor, I.T.P.I Building, Beside Celebration Mall, Bhuwana, Udaipur, Rajasthan - 313001'''


def leaveForwardmessage(username, startdate, enddate):
    return '''
    Hello ''' + username + ''',
        
    After reviewing your request for leave, I am unable to grant your leave from ''' + startdate.split('T')[0] + '''  to  ''' + enddate.split('T')[0] + '''. I need to forward your application to higher authority for grant. You will shortly receive mail regarding Accept/Reject your application. We appreciate your thoughtfulness to inform us well in advance.

    If you have any queries, please feel free to contact the Human Resources  Department. We look forward to your success in the company\n

    Thanks & Regards,
    Name of hr
    HR Executive 
    Direct: +91 6353235503 | W: www.lanetteam.com 
    406, Luxuria Business Hub, Nr. VR Mall, Surat, Gujarat - 395007. Ground Floor, I.T.P.I Building, Beside Celebration Mall, Bhuwana, Udaipur, Rajasthan - 313001'''
