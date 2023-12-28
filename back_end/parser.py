# #############################################################################
# Parser has functions for taking a string then passing that with mathematical
# options in a predescribed manner. Customizable for number type.
# #############################################################################

import regex as re
from decimal import Decimal
import logging

logging.getLogger().setLevel(logging.DEBUG)


# Exceptions
class FormulaParsingError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


class UnknownDigitTypeError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


def make_regex(s2r):
    regex_str = ''
    for c in s2r:
        if c in r".-^$*+?()[]{}\|":
            regex_str += "\\" + c
        else:
            regex_str += c
    return regex_str


def make_re_opts(s2r):
    regex_str = ''
    for g in s2r:
        regex_str += make_regex(g) + '|'
    return regex_str[:-1]


def parenth_calc(formula_text, start_par_sym="(", end_par_sym=")",
                 digit_type=float, pow_sym="**", div_sym="/",
                 mul_sym="*", add_sym="+", sub_sym="-"):
    logging.debug("parenth_calc started")
    parse_array = ['']
    for c in formula_text:
        if c != start_par_sym and c != end_par_sym:
            parse_array[-1] += c
        elif c == start_par_sym:
            parse_array.append('')
        elif c == end_par_sym:
            try:
                parse_array[-2] += calculate(parse_array[-1],
                                             start_par_sym=start_par_sym,
                                             end_par_sym=end_par_sym,
                                             digit_type=digit_type,
                                             pow_sym=pow_sym,
                                             div_sym=div_sym,
                                             mul_sym=mul_sym,
                                             add_sym=add_sym,
                                             sub_sym=sub_sym)
                parse_array.pop()
            except IndexError:
                raise FormulaParsingError("Balanced Parentheses Error: "
                                          + "Too many closing brackets")
        else:
            raise FormulaParsingError("FATAL CODE ERROR: Logic error with " +
                                      "parsing function")
    logging.debug("parenth_calc ended-returned: " + parse_array[0])
    return parse_array[0]


def calculate(formula_text, digit_type=float, start_par_sym="(",
              end_par_sym=")", pow_sym="**", div_sym="/",
              mul_sym="*", add_sym="+", sub_sym="-"):
    logging.info("STARTED: calculate")

    if digit_type == float or digit_type == Decimal:
        num_chars = '0123456789'
        sep_point = '.'
        neg_sym = '-'
    elif digit_type == int:
        num_chars = '0123456789'
        sep_point = '.'
        neg_sym = '-'
    else:
        try:
            num_chars = digit_type.ssys.digit_list
            sep_point = digit_type.ssys.sep_point
            neg_sym = digit_type.ssys.neg_sym
        except Exception:
            raise UnknownDigitTypeError("Digit characters not known")
    logging.debug("  num_chars: " + num_chars)
    logging.debug("  sep_point: " + sep_point)
    logging.debug("  neg_sym: " + neg_sym)

    # Order also defines order in which they're calculated. Exponent must
    # always be first to account for (-x)**y cases
    ops = {pow_sym: digit_type.__pow__,
           div_sym: digit_type.__truediv__,
           mul_sym: digit_type.__mul__,
           sub_sym: digit_type.__sub__,
           add_sym: digit_type.__add__,
           }
    op_parse_dirctn = {pow_sym: 'left',
                       div_sym: 'right',
                       mul_sym: 'right',
                       add_sym: 'right',
                       sub_sym: 'right',
                       }

    pos_dig_regex = ('[' + num_chars + ']+(' + make_regex(sep_point) + '['
                     + num_chars + ']+)?')
    expn_regex = ('(' + make_regex(start_par_sym) + make_regex(neg_sym) + '?'
                  + pos_dig_regex + make_regex(end_par_sym)
                  + make_regex(pow_sym) + pos_dig_regex + ')')
    logging.debug("  expn_regex: " + expn_regex)

    # Added section to account for exponents of negated number in parentheses
    if re.findall(expn_regex, formula_text):
        exp_arr = [e[0] for e in re.findall(expn_regex, formula_text)]
        logging.debug("  Exp instancs: " + str(exp_arr))
        exp_form_arr = re.split(expn_regex, formula_text)
        logging.debug("  exp_form_arr: " + str(exp_form_arr))
        formula_text = ''
        for exp_ind in range(0, len(exp_arr)):
            base = re.search('(?<=' + make_regex(start_par_sym) + ')'
                             + make_regex(neg_sym) + '?' + pos_dig_regex,
                             exp_arr[exp_ind])[0]
            expn = re.search(make_regex(neg_sym) + '?' + pos_dig_regex + '$',
                             exp_arr[exp_ind])[0]
            formula_text += (exp_form_arr[exp_ind]
                             + str(digit_type.__pow__(digit_type(base),
                                                      digit_type(expn))))
        formula_text += exp_form_arr[-1]
        logging.info("  Post prelim exp formula: " + formula_text)

    formula_text = parenth_calc(formula_text, start_par_sym=start_par_sym,
                                end_par_sym=end_par_sym, digit_type=digit_type,
                                pow_sym=pow_sym, div_sym=div_sym,
                                mul_sym=mul_sym, add_sym=add_sym,
                                sub_sym=sub_sym)
    logging.info(" Post parenth formula: " + formula_text)

    operator_set = [k for k in ops.keys()]
    logging.debug("  operator_set: " + str(operator_set))

    sym_loop_counter = 0

    # Added to initialize so can be recursive in following loop
    split_fml = [formula_text]

    for sym in operator_set:
        sym_loop_counter += 1
        sym_split_regex = ('(?<!^|' + make_re_opts(operator_set) + ')'
                           + make_regex(sym))
        logging.debug('    Ops Split Regex: ' + sym_split_regex)
        logging.debug('    split_fml: ' + str(split_fml))
        split_fml = re.split(sym_split_regex, split_fml[0])
        logging.debug("  Formula Split on " + sym + " :"
                      + str(sym_loop_counter) + ": " + str(split_fml))

        if len(split_fml) > 1:
            if op_parse_dirctn[sym] == 'left':
                parse_order = range(1, len(split_fml))[::-1]
            elif op_parse_dirctn[sym] == 'right':
                parse_order = [1] * (len(split_fml) - 1)
            else:
                raise Exception("Parse direction dictionary should be "
                                + "fixed to have 'left' or 'right'")

            for fml_ind in parse_order:
                num_pattern = ('(((?<=(^|[' + make_re_opts(operator_set)
                               + ']))(' + make_regex(neg_sym) + ')?)?['
                               + make_regex(num_chars) + ']+('
                               + make_regex(sep_point) + '['
                               + make_regex(num_chars) + ']+)?)')
                logging.debug("  num_pattern: " + num_pattern)

                # Condition added to account for precedence of exponentiation
                # over negation
                if sym == pow_sym:
                    base_regex = ('([' + make_regex(num_chars) + ']+('
                                  + make_regex(sep_point) + '['
                                  + make_regex(num_chars) + ']+)?)$')
                    logging.debug("  base_regex: " + base_regex)
                    base = re.findall(base_regex, split_fml[fml_ind - 1])[0][0]
                    logging.debug("  Exp in prior: " + str(base))
                    input1 = base
                else:
                    input1 = re.findall(num_pattern + '$',
                                        split_fml[fml_ind - 1])[0][0]
                logging.debug("    input1: " + str(input1))
                input2 = re.findall('^' + num_pattern,
                                    split_fml[fml_ind])[0][0]
                logging.debug("    input2: " + str(input2))

                if sym == pow_sym:
                    new_prior = re.sub(base_regex, '',
                                       split_fml[fml_ind - 1], 1)
                else:
                    new_prior = re.sub(num_pattern + '$', '',
                                       split_fml[fml_ind - 1], 1)
                logging.debug("    new_prior: " + new_prior)
                new_post = re.sub('^' + num_pattern, '',
                                  split_fml[fml_ind], 1)
                logging.debug("    new_post: " + new_post)

                calc = str(ops[sym](digit_type(input1), digit_type(input2)))
                logging.debug("    calc: " + calc)

                if op_parse_dirctn[sym] == 'left':
                    split_fml[fml_ind - 1] = (new_prior + calc + new_post)
                    split_fml.pop()
                elif op_parse_dirctn[sym] == 'right':
                    split_fml[1] = (new_prior + calc + new_post)
                    split_fml = split_fml[fml_ind:]
                else:
                    raise Exception("Parse direction dictionary should be "
                                    + "fixed to have 'left' or 'right'")
        logging.info("  Post " + sym + " parse formula: " + split_fml[0])
    logging.info("ENDED: calculate Returned: " + str(split_fml[0]))
    return split_fml[0]
