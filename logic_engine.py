class KnowledgeBase:
    """
    Knowledge Base for storing facts and rules.

    Facts:
        Stored as a set of strings.

    Rules:
        Stored as tuples:
        (premise_list, conclusion)
    """

    def __init__(self):
        self.facts = set()
        self.rules = []

    def tell_fact(self, fact_string):
        """
        Add a fact to the knowledge base.
        """
        self.facts.add(fact_string)

    def tell_rule(self, premise_list, conclusion_string):
        """
        Add a rule to the knowledge base.

        Example:
            ['TargetVisible', 'HasDust']
            -> 'SafeToEngage'
        """
        self.rules.append(
            (premise_list, conclusion_string)
        )

    def clear_facts(self):
        """
        Remove all current facts.
        Rules remain unchanged.
        """
        self.facts.clear()

    def forward_chain(self):
        """
        Forward Chaining inference.

        Continues applying rules until no
        new facts can be deduced.
        """

        new_facts_added = True

        while new_facts_added:

            new_facts_added = False

            for premises, conclusion in self.rules:

                # Do not add an existing fact again
                if conclusion in self.facts:
                    continue

                # Modus Ponens:
                # If ALL premises are true,
                # conclude the rule's conclusion.
                if all(
                    premise in self.facts
                    for premise in premises
                ):

                    self.facts.add(
                        conclusion
                    )

                    new_facts_added = True