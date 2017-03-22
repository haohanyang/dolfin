// Copyright (C) 2016 Chris Richardson
//
// This file is part of DOLFIN.
//
// DOLFIN is free software: you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// DOLFIN is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
// GNU Lesser General Public License for more details.
//
// You should have received a copy of the GNU Lesser General Public License
// along with DOLFIN. If not, see <http://www.gnu.org/licenses/>.
//

#ifndef __PETSC_NESTMATRIX_H
#define __PETSC_NESTMATRIX_H

#ifdef HAS_PETSC

#include <petscmat.h>
#include <petscsys.h>

#include "PETScMatrix.h"

namespace dolfin
{
  class GenericMatrix;
  class GenericVector;
  class FunctionSpace;

  /// PETScNestMatrix creates an NxN nested matrix from a list
  /// of 'sub-matrices' in order from top left down to bottom right.
  /// Therefore the number of matrices supplied must be a perfect
  /// square. If any matrices are empty, a NULL pointer can be supplied.

  class PETScNestMatrix : public PETScMatrix
  {
  public:

    /// Create empty matrix
    PETScNestMatrix();

    /// Create from a list of matrices and FunctionSpaces
    explicit PETScNestMatrix
      (std::vector<std::shared_ptr<const GenericMatrix>> mats);

    /// Destructor
    virtual ~PETScNestMatrix();

    /// Multiply
    virtual void mult(const GenericVector& x, GenericVector& y) const;

    /// Initialise a nest vector for use with matrix
    void init_vectors(GenericVector& z_out,
                      std::vector<std::shared_ptr<const GenericVector>> z_in) const;

    /// Get dofs for each block
    void get_block_dofs(std::vector<dolfin::la_index>& dofs, std::size_t idx) const;

    /// Return size of given dimension
    std::size_t size(std::size_t dim) const
    { return PETScBaseMatrix::size(dim); }

    /// Description
    virtual std::string str(bool verbose) const;

  };

}

#endif

#endif
