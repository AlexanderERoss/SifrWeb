# #############################################################################
# Parser has functions for taking a string then passing that with mathematical
# options in a predescribed manner. Customizable for number type.
# #############################################################################

import regex as re
from decimal import Decimal
import logging

logging.getLogger().setLevel(logging.WARNING)


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
                parse_array[-2] += base_calc(parse_array[-1])
                parse_array.pop()
            except IndexError:
                raise FormulaParsingError("Balanced Parentheses Error: "
                                          + "Too many closing brackets")
        else:
            raise FormulaParsingError("FATAL CODE ERROR: Logic error with " +
                                      "parsing function")
    logging.debug("parenth_calc ended-returned: " + parse_array[0])
    return parse_array[0]


def base_calc(formula_text, digit_type=float, pow_sym="**", div_sym="/",
              mul_sym="*", add_sym="+", sub_sym="-"):
    logging.debug("base_calc started")
    ops = {pow_sym: digit_type.__pow__,
           div_sym: digit_type.__truediv__,
           mul_sym: digit_type.__mul__,
           add_sym: digit_type.__add__,
           sub_sym: digit_type.__sub__,
           }
    op_parse_dirctn = {pow_sym: 'left',
                       div_sym: 'right',
                       mul_sym: 'right',
                       add_sym: 'right',
                       sub_sym: 'right',
                       }
    operator_set = [k for k in ops.keys()]
    logging.debug("  operator_set: " + str(operator_set))

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
            num_chars = digit_type.digit_list
            sep_point = digit_type.sep_point
            neg_sym = digit_type.neg_sym
        except Exception as e:
            raise UnknownDigitTypeError("Digit characters not known: "
                                        + e.message)
    logging.debug("  num_chars: " + num_chars)
    logging.debug("  sep_point: " + sep_point)
    logging.debug("  neg_sym: " + neg_sym)

    sym_loop_counter = 0

    # Added to initialize so can be recursive in following loop
    split_fml = [formula_text]

    for sym in operator_set:
        sym_loop_counter += 1
        sym_split_regex = ('(?<!' + make_re_opts(operator_set) + ')'
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

                input1 = re.findall(num_pattern + '$',
                                    split_fml[fml_ind - 1])[0][0]
                logging.debug("    input1: " + str(input1))
                input2 = re.findall('^' + num_pattern,
                                    split_fml[fml_ind])[0][0]
                logging.debug("    input2: " + str(input2))

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
                logging.debug("  Loop ended: split_fml: " + str(split_fml))
    logging.debug("base_calc ended-returned: " + str(split_fml[0]))
    return split_fml[0]
