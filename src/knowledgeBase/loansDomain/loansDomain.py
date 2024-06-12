from knowledgeBase.commons.decision import Decision
from knowledgeBase.commons.case import Case
from knowledgeBase.commons.criteria import Criteria

"""Client age
"""
class Age(Case):
    def __init__(self):
        super(Age, self).__init__('edad del cliente', 'natural')

"""Amount of money that the client has in the bank
"""
class Amount(Case):
    def __init__(self):
        super(Amount, self).__init__('cuantía del cliente', 'real')

"""Annual incomes of the client
"""
class AnnualIncomes(Case):
    def __init__(self):
        super(AnnualIncomes, self).__init__('ingresos anuales', 'real')

"""Number of times that the client have not paid their debts
"""
class Defaults(Case):
    def __init__(self):
        super(Defaults, self).__init__('número de impagos', 'natural')

"""Current debt of the client
"""
class Debt(Case):
    def __init__(self):
        super(Debt, self).__init__('deuda', 'real')

"""Employment situation of the client
"""
class EmploymentStatus(Case):
    def __init__(self):
        super(EmploymentStatus, self).__init__('situación laboral', 'selectable', ['desempleado', 'temporal', 'indefinido', 'fijo', 'autónomo/empresario'])

"""Amount of money requested
"""
class LoanAmount(Case):
    def __init__(self):
        super(LoanAmount, self).__init__('cuantía del préstamo', 'real')

"""Loan duration in years
"""
class LoanDuration(Case):
    def __init__(self):
        super(LoanDuration, self).__init__('duración del préstamo', 'natural')

def getCases():
    """Function that returns the cases for the loan domain

        Returns:
            Array<Case>: List of cases
        """
    cases=[]
    cases.append(Age())
    cases.append(Amount())
    cases.append(AnnualIncomes())
    cases.append(EmploymentStatus())
    cases.append(Defaults())
    cases.append(Debt())
    cases.append(LoanAmount())
    cases.append(LoanDuration())
    
    return cases

"""Criteria for age of the client when the loan have been paid
"""
class EndLoanCriteria(Criteria):
    def __init__(self):
        """Constructor
        """
        super(EndLoanCriteria, self).__init__('edad de finalizanción del préstamo')

    def eval(self, case, decision: Decision):
        """Redefinition of eval method

        Args:
            case (Array<(key,value)>): Case information
            decision (Decision): Current decision

        Returns:
            Decision: New decision
        """
        super(EncodingWarning, self).eval(case, decision)

        clientAge = -1
        loanDuration = -1
        message = f'evaluando {self.name}\n\t'

        for i in range(len(case)):
            if(case[i][0] == 'edad del cliente'):
                clientAge = int(case[i][1])
            elif(case[i][0] == 'duración del préstamo'):
                loanDuration = int(case[i][1])
        
        if(clientAge < 0 or loanDuration < 0):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}No se ha especificado la edad del cliente o la duración del préstamo\n'
        elif (clientAge + loanDuration > 80):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}Denegado debido a que la edad de finalización del préstamo es mayor a 80 años\n'
        else:
            decision.setDecision(True)
            message = '{message}Edad de finalización del préstamo válida\n'
        
        return decision, message
    
"""Criteria for unemployed status
"""  
class UnemployedCriteria(Criteria):
    def __init__(self):
        """Constructor
        """
        super(UnemployedCriteria, self).__init__('cliente no desempleado')
    
    def eval(self, case, decision: Decision):
        """Redefinition of eval method

        Args:
            case (Array<(key,value)>): Case information
            decision (Decision): Current decision

        Returns:
            Decision: New decision
        """
        super(UnemployedCriteria, self).eval(case, decision)

        employmentStatus = -''
        message = f'evaluando {self.name}\n\t'

        for i in range(len(case)):
            if(case[i][0] == 'situación laboral'):
                employmentStatus = case[i][1]
        
        if(employmentStatus == ''):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}No se ha especificado la situación laboral del cliente\n'
        elif (employmentStatus == 'desempleado'):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}Denegado debido a que el cliente se encuentra en situación de desempleo\n'
        else:
            decision.setDecision(True)
            message = '{message}Situación laboral válida\n'
        
        return decision, message

"""Criteria for employment status
"""
class EmploymentStatusCriteria(Criteria):
    def __init__(self):
        """Constructor
        """
        super(EmploymentStatusCriteria, self).__init__('situación laboral del cliente')
    
    def eval(self, case, decision: Decision):
        """Redefinition of eval method

        Args:
            case (Array<(key,value)>): Case information
            decision (Decision): Current decision

        Returns:
            Decision: New decision
        """
        super(EmploymentStatusCriteria, self).eval(case, decision)

        employmentStatus = -''
        message = f'evaluando {self.name}\n\t'

        for i in range(len(case)):
            if(case[i][0] == 'situación laboral'):
                employmentStatus = case[i][1]
        
        if(employmentStatus == ''):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}No se ha especificado la situación laboral del cliente\n'
        elif (employmentStatus == 'desempleado'):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}Denegado debido a que el cliente se encuentra en situación de desempleo\n'
        elif(employmentStatus == 'fijo'):
            decision.setDecision(True)
            decision.addDetail('interés', 0.02)
            message = '{message}Situación laboral válida\n'
        elif(employmentStatus == 'indefinido' or employmentStatus == 'autónomo/empresario'):
            decision.setDecision(True)
            decision.addDetail('interés', 0.025)
            message = '{message}Situación laboral válida\n'
        elif(employmentStatus == 'temporal'):
            decision.setDecision(True)
            decision.addDetail('interés', 0.035)
            message = '{message}Situación laboral válida\n'
        else:
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}Situación laboral incorrecta\n'

        
        return decision, message

"""Criteria for the number of times that the client has not paid his debts
"""
class DefaultsCriteria(Criteria):
    def __init__(self):
        """Constructor
        """
        super(DefaultsCriteria, self).__init__('número de impagos')
    
    def eval(self, case, decision: Decision):
        """Redefinition of eval method

        Args:
            case (Array<(key,value)>): Case information
            decision (Decision): Current decision

        Returns:
            Decision: New decision
        """
        super(DefaultsCriteria, self).eval(case, decision)

        defaults = -1
        message = f'evaluando {self.name}\n\t'
        interest = decision.getDetail('interest')

        for i in range(len(case)):
            if(case[i][0] == 'número de impagos'):
                defaults = case[i][1]
        
        if(defaults == -1):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}No se ha especificado el número de impagos\n'
        else:
            interest = decision.getDetail('interest')

            decision.setDecision(True)
            decision.addDetail('interés', interest + (defaults * 0.003))
            message = '{message}Número de impagos evaluado\n'

        return decision, message

"""Criteria for the amount of money the client could request
"""
class AmountCriteria(Criteria):
    def __init__(self):
        """Constructor
        """
        super(AmountCriteria, self).__init__('cuantía solicitada')
    
    def eval(self, case, decision: Decision):
        """Redefinition of eval method

        Args:
            case (Array<(key,value)>): Case information
            decision (Decision): Current decision

        Returns:
            Decision: New decision
        """
        super(AmountCriteria, self).eval(case, decision)

        monthyPayment = decision.getDetail('cuantía mensual')
        duration = decision.getDetail('duración')
        debts = -1
        annualIncomes = -1

        for i in range(len(case)):
            if(case[i][0] == 'ingresos anuales'):
                annualIncomes = case[i][1]
            elif(case[i][0] == 'deuda'):
                debts = case[i][1]

            if(debts != -1 and annualIncomes != -1):
                break
        
        if(debts == -1 or annualIncomes == -1):
            decision.setDecision(False)
            decision.setDecisionMade(True)
            message = '{message}No se ha especificado el salario anual o la deuda actual\n'
        elif (monthyPayment * 12 * duration > 0.5 * ((annualIncomes * duration) - debts)):
            decision.setDecision(False)
            decision.setDecisionMade(True)

            message = '{message}Se ha solicitado demasiado dinero para sus posibilidades\n'
        else:
            decision.setDecision(True)

            message = '{message}El préstamo entra dentro de sus posibilidades\n'

        return decision, message
    
def getCriterias():
    """Function that returns all criterias
    
    Returns:
        Array<Criterias>: All criterias
    """
    criterias = []
    criterias.append(EndLoanCriteria())
    criterias.append(UnemployedCriteria())
    criterias.append(EmploymentStatusCriteria())
    criterias.append(DefaultsCriteria())
    criterias.append(AmountCriteria())

    return criterias


"""Decision class for loans domain
"""
class LoanDecision(Decision):
    """Decision class construtor

    Args:
        decision (bool, optional): Value that represents the decision. Defaults to False.
    """
    def __init__(self, decision: bool = False):
        super(LoanDecision, self).__init__(decision, [('cantidad', 0), ('duración', 0), ('interés', 0), ('cuantía mensual', 0)])
    """Overwrites toString method from Decision class
    """
    def toString(self):
        self.calcInterest()
        if(self._decision):
            message = 'Decisión: Concedido\n\n'
            for key, value in self._details:
                message += f'\t{key}: {value}\n'
        else:
            return 'Decisión: Denegado'
    def addDetail(self, key: str, value):
        super().addDetail(key, value)

        self.recalcMonthyPayment()

    def recalcMonthyPayment(self):
        interest = self.getDetail('interés')
        amount = self.getDetail('cantidad')
        monthPayPos = -1
        duration = self.getDetail('duración')

        for i in range(len(self._details)):
            if self._details[i][0] == 'cuantía mensual':
                monthPayPos = i
                break
        
        self._details[monthPayPos][1] = (amount + (amount * ((interest) + 1) ** duration)) / 12 * duration