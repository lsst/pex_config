// -*- lsst-c++ -*-
/*
 * This file is part of pex_config.
 *
 * Developed for the LSST Data Management System.
 * This product includes software developed by the LSST Project
 * (http://www.lsst.org).
 * See the COPYRIGHT file at the top-level directory of this distribution
 * for details of code ownership.
 */

#ifndef LSST_PEX_CONFIG_PYTHON_H
#define LSST_PEX_CONFIG_PYTHON_H

/**
 * Macro used to wrap fields declared by `LSST_CONTROL_FIELD` using Pybind11.
 *
 * Example:
 *
 *     LSST_DECLARE_CONTROL_FIELD(clsFoo, Foo, myField)
 *
 * @param WRAPPER The py::class_ object representing the control class being
 *                wrapped.
 * @param CLASS The control class. Must be a C++ identifier (not a string),
 *              properly namespace-qualified for the context where this macro
 *              is being called.
 * @param NAME The control field. Must be a C++ identifier (not a string), and
 *             must match the `NAME` argument of the original
 *             `LSST_CONTROL_FIELD` macro.
 */
#define LSST_DECLARE_CONTROL_FIELD(WRAPPER, CLASS, NAME)         \
    WRAPPER.def_readwrite(#NAME, &CLASS::NAME);                  \
    WRAPPER.def_static("_doc_" #NAME, &CLASS::_doc_ ## NAME);    \
    WRAPPER.def_static("_type_" #NAME, &CLASS::_type_ ## NAME);

/**
 * Macro used to wrap fields declared by `LSST_NESTED_CONTROL_FIELD` using
 * Pybind11.
 *
 * Example:
 *
 *     LSST_DECLARE_NESTED_CONTROL_FIELD(clsFoo, Foo, myField)
 *
 * @param WRAPPER The py::class_ object representing the control class being
 *                wrapped.
 * @param CLASS The control class. Must be a C++ identifier (not a string),
 *              properly namespace-qualified for the context where this macro
 *              is being called.
 * @param NAME The control field. Must be a C++ identifier (not a string), and
 *             must match the `NAME` argument of the original
 *             `LSST_CONTROL_FIELD` macro.
 */
#define LSST_DECLARE_NESTED_CONTROL_FIELD(WRAPPER, CLASS, NAME)  \
    WRAPPER.def_readwrite(#NAME, &CLASS::NAME);                  \
    WRAPPER.def_static("_doc_" #NAME, &CLASS::_doc_ ## NAME);    \
    WRAPPER.def_static("_type_" #NAME, &CLASS::_type_ ## NAME);  \
    WRAPPER.def_static("_module_" #NAME, &CLASS::_module_ ## NAME);

#endif
