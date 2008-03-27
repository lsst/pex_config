// -*- lsst-c++ -*-
%define logging_DOCSTRING
"
Access to the policy classes from the mwi library
"
%enddef

%feature("autodoc", "1");
%module(package="lsst.mwi", docstring=logging_DOCSTRING) policy

%{
#include "lsst/mwi/policy/Policy.h"
#include "lsst/mwi/policy/PolicyFile.h"
#include "lsst/mwi/utils/Trace.h"
#include "lsst/mwi/policy/exceptions.h"
%}

%inline %{
namespace lsst { namespace mwi { namespace data { } } }
namespace lsst { namespace mwi { namespace policy { } } }
namespace lsst { namespace mwi { namespace utils { } } }
namespace boost { namespace filesystem { } }

using namespace lsst;
using namespace lsst::mwi::data;
using namespace lsst::mwi::policy;
using namespace lsst::mwi::utils;
%}

%init %{
%}
%pythoncode %{
import lsst.mwi.utils
import lsst.mwi.data
%}

%include "p_lsstSwig.i"
%import  "data.i"

%typemap(out) std::vector<double,std::allocator<double > >& {

    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    int i;
    for (i = 0; i < len; i++) {
        PyList_SetItem($result,i,PyFloat_FromDouble((*$1)[i]));
    }
}

%typemap(out) std::vector<int,std::allocator<int > >& {

    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    int i;
    for (i = 0; i < len; i++) {
        PyList_SetItem($result,i,PyInt_FromLong((*$1)[i]));
    }
}

%typemap(out) std::vector<boost::shared_ptr<string > >& {

    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    int i;
    for (i = 0; i < len; i++) {
        PyList_SetItem($result,i,PyString_FromString((*$1)[i]->c_str()));
    }
}

%typemap(out) std::vector<bool,std::allocator<bool > >& {

    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    int i;
    for (i = 0; i < len; i++) {
        PyList_SetItem($result,i, ( ((*$1)[i]) ? Py_True : Py_False ) );
    }
}

%typemap(out) std::vector<boost::shared_ptr<lsst::mwi::policy::Policy > >& {

    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    int i;
    PyObject *pol;
    for (i = 0; i < len; i++) {
        pol = SWIG_NewPointerObj(SWIG_as_voidptr((*$1)[i].get()),
                                 SWIGTYPE_p_lsst__mwi__policy__Policy,
                                 0 );
        PyList_SetItem($result,i, pol);
    }
}

%typemap(out) boost::shared_ptr<lsst::mwi::policy::Policy >& {

    // unwrap the shared pointer
    $result = SWIG_NewPointerObj(SWIG_as_voidptr((*$1).get()),
                                 SWIGTYPE_p_lsst__mwi__policy__Policy,
                                 0 );
}

%typemap(in,numinputs=0) std::list<std::string > &names (std::list<std::string > temp) {
    $1 = &temp;
}

%typemap(argout) std::list<std::string > &names {
    int len = (*$1).size();  // swig presents $1 as a pointer
    $result = PyList_New(len);
    std::list<std::string >::iterator sp;
    int i = 0;
    for (sp = (*$1).begin(); sp != (*$1).end(); sp++, i++) {
        PyList_SetItem($result,i,PyString_FromString(sp->c_str()));
    }
}

%include "exception.i"
%include "lsst/mwi/policy/exceptions.h"

%exception {
    try {
        $action;
    } catch (NameNotFound &e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (TypeError &e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (BadNameError &e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (IOError &e) {
        SWIG_exception(SWIG_RuntimeError, e.what());
    } catch (std::exception &e) {
        SWIG_exception(SWIG_RuntimeError, 
   string(e.what()).append(" (").append(typeid(e).name()).append(")").c_str());
    } catch (...) {
       SWIG_exception(SWIG_RuntimeError, "unknown error while handling policy");
    }
}
        
%include "lsst/mwi/data/Citizen.h"

%newobject lsst::mwi::policy::Policy::createPolicy;

%include "lsst/mwi/policy/Policy.h"
%include "lsst/mwi/policy/PolicySource.h"
%include "lsst/mwi/policy/PolicyFile.h"

%extend lsst::mwi::policy::Policy {
    string toString() {
       ostringstream msg;
       self->print(msg);
       return msg.str();
    }
}

%template(PolicySharedPtr) boost::shared_ptr<lsst::mwi::policy::Policy>;
%template(NameList) std::list<std::string >;

%pythoncode %{
Policy.__str__ = Policy.toString

def _Policy_get(p, name, defval=None):
    type = p.getValueType(name);
    if (type == p.UNDEF):  return defval

    if (type == p.INT):
        return p.getInt(name)
    elif (type == p.DOUBLE):
        return p.getDouble(name)
    elif (type == p.BOOL):
        return p.getBool(name)
    elif (type == p.STRING):
        return p.getString(name)
    elif (type == p.POLICY):
        return p.getPolicy(name)

def _Policy_getArray(p, name, defarray=None):
    type = p.getValueType(name);
    if (type == p.UNDEF):  return defarray

    if (type == p.INT):
        return p.getIntArray(name)
    elif (type == p.DOUBLE):
        return p.getDoubleArray(name)
    elif (type == p.BOOL):
        return p.getBoolArray(name)
    elif (type == p.STRING):
        return p.getStringArray(name)
    elif (type == p.POLICY):
        return p.getPolicyArray(name)

Policy.get = _Policy_get
Policy.getArray = _Policy_getArray
PolicySharedPtr.get = _Policy_get
PolicySharedPtr.getArray = _Policy_getArray

def PolicyPtr(*args):
    """return a PolicySharedPtr that owns its own Policy"""
    return PolicySharedPtr(Policy(*args))

%}

